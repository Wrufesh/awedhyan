// fields = ('id', 'detail', 'is_correct')
var get_course_chapters = function (course_id, defaultCallback) {
    var failureCallback = function (err) {
        var err_message = err.responseJSON.detail;
        var error = App.notifyUser(
            err_message,
            'error'
        );
        App.hideProcessing();
    };
    var url = '/api/coursechapters/?course_id=' + String(course_id);
    App.remoteGet(url, {}, defaultCallback, failureCallback);
};

function Choice() {
    var self = this;
    self.id = ko.observable();
    self.detail = ko.observable();
    self.is_correct = ko.observable(false);

}

function TestChapterQuestion() {
    var self = this;
    self.id = ko.observable();
    // This is observable of question ID
    self.question = ko.observable();
    self.points = ko.observable();
}

function TestNonChapterQuestion() {
    var self = this;
    self.id = ko.observable();
    self.points = ko.observable();
    // This is observable of question object
    self.question = ko.observable();
}

// fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')
function Question() {
    var self = this;

    self.id = ko.observable();
    self.detail = ko.observable();
    // self.image = ko.observable();
    self.image = ko.observable({
        dataURL: ko.observable()
    });
    self.true_false_answer = ko.observable(false);
    self.type = ko.observable();
    self.choices = ko.observableArray();
    self.errors = ko.observableArray();

    self.choices_to_delete = ko.observableArray();

    self.type.subscribe(function () {
        if (self.type() == 'TRUE/FALSE' || self.type() == 'ESSAY') {
            self.choices([]);
        }
        if (self.type() == 'OBJECTIVE') {
            self.choices.push(new Choice());
            self.true_false_answer(false);
        }
        if (self.type() == 'ESSAY') {
            self.true_false_answer(false);
            self.choices([]);
        }

    });

    self.add_choice = function () {
        self.choices.push(new Choice())
    };

    self.remove_choice = function (choice) {
        if (choice.id()) {
            self.choices_to_delete.push(choice.id());
        }
        self.choices.remove(choice);
    }

    // self.errors.subscribe(function () {
    //     if(self.errors.length > 0){
    //         self.question_error_class('bg-error')
    //     }else{
    //         self.question_error_class('bg-faded')
    //     }
    // })
}
// fields = ('id', 'name', 'course', 'pass_mark', 'questions')
function Test() {
    var self = this;
    self.id = ko.observable();
    self.name = ko.observable();
    self.chapters = ko.observableArray();
    self.course = ko.observable();
    self.pass_marks = ko.observable();
    self.chapter_questions = ko.observableArray();
    self.non_chapter_questions = ko.observableArray();

    self.selected_course_chapter_questions = ko.observableArray();

    self.course.subscribe(function () {
        console.log('hey');
        if (self.course()) {
            get_course_chapters(self.course(), function (response) {
                console.log(response);
                var modified_response = ko.utils.arrayMap(response, function (chapter) {
                    var modified_questions = ko.utils.arrayMap(chapter.questions, function (question) {
                        question['is_selected'] = ko.observable();
                        question['points'] = ko.observable();

                        return question
                    });

                    chapter.questions = modified_questions;

                    return chapter
                });
                console.log(modified_response);
                self.selected_course_chapter_questions(modified_response)
            });
        }
    });

    self.add_non_chapter_question = function () {
        self.non_chapter_questions.push(new Question());
    };

    self.remove_non_chapter_question = function (question) {
        if (question.id()) {
            self.questions_to_delete.push(question.id());
        }
        self.questions.remove(question)
    };

    self.validation = function () {
        var valid = true;
        ko.utils.arrayForEach(self.questions(), function (question) {
            if (question.type() == 'OBJECTIVE') {
                var has_no_correct_choice = true;
                ko.utils.arrayForEach(question.choices(), function (choice) {
                    if (choice.is_correct()) {
                        has_no_correct_choice = false;
                    }
                });
                if (has_no_correct_choice) {
                    valid = false;
                    question.errors.push('Atleast one correct choice needed.');
                } else {
                    question.errors([]);
                }
            }

        });
        return valid
    };

    self.save = function () {
        if (self.validation()) {
            App.showProcessing();
            var payload = ko.toJSON(self);
            var url = '/academy/chapterquestions/add/' + String(self.chapter_id()) + '/';


            var defaultCallback = function (response) {
                if (response.success) {
                    App.hideProcessing();
                    App.notifyUser('Succesfully Saved', 'success');
                }
            };
            var failureCallback = function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            };
            App.remoteMultipartPost(url, payload, defaultCallback, failureCallback);
        }


    };

}