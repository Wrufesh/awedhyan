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

function TestChapterQuestion(data) {
    var self = this;
    self.id = ko.observable();
    // This is observable of question ID
    self.question = ko.observable();
    self.chapter = ko.observable();
    self.points = ko.observable();

    if (data) {
        for (var i in data) {
            self[i](data[i])
        }
    }
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

function TestNonChapterQuestion() {
    var self = this;
    self.id = ko.observable();
    self.points = ko.observable();
    // This is observable of question object
    self.question = ko.observable(new Question());
}

// fields = ('id', 'name', 'course', 'pass_mark', 'questions')
function Test() {
    var self = this;
    self.id = ko.observable();
    self.name = ko.observable();
    self.course = ko.observable();
    self.pass_mark = ko.observable();
    self.chapter_questions = ko.observableArray();
    self.non_chapter_questions = ko.observableArray();

    self.selected_course_chapter_questions = ko.observableArray();
    self.test_questions_to_delete = ko.observableArray();

    self.update_selected_chapter_questions = function () {
        var new_chapter_questions = [];
        ko.utils.arrayForEach(self.selected_course_chapter_questions(), function (chapter) {
            ko.utils.arrayForEach(chapter.questions, function (question) {
                if (question.is_selected()) {
                    var data = {
                        'id': question.test_question_id(),
                        'question': question.id,
                        'chapter': chapter.id,
                        'points': question.points
                    };
                    new_chapter_questions.push(new TestChapterQuestion(data))
                } else {
                    if (typeof(question.test_question_id()) != 'undefined') {
                        self.test_questions_to_delete.push(question.test_question_id())
                    }
                }
            })
        });
        self.chapter_questions(new_chapter_questions)
    };

    self.course.subscribe(function () {
        if (self.course()) {
            get_course_chapters(self.course(), function (response) {
                console.log(response);

                var modified_response = ko.utils.arrayMap(response, function (chapter) {
                    var modified_questions = ko.utils.arrayMap(chapter.questions, function (question) {
                        question.test_question_id = ko.observable()
                        question['is_selected'] = ko.observable();
                        question['points'] = ko.observable();
                        question.points.subscribe(self.update_selected_chapter_questions);
                        question.is_selected.subscribe(self.update_selected_chapter_questions);

                        return question
                    });

                    chapter.questions = modified_questions;

                    return chapter
                });
                self.selected_course_chapter_questions(modified_response)

                ko.utils.arrayForEach(self.selected_course_chapter_questions(), function (chapter) {
                    ko.utils.arrayForEach(chapter.questions, function (question) {
                        ko.utils.arrayForEach(self.chapter_questions(), function (chapter_question) {
                            if (chapter_question.question == question.id) {
                                question.is_selected(true);
                                question.points(chapter_question.points());
                                question.test_question_id(chapter_question.id())
                            }
                        })
                    })
                });
            });
        }
    });

    self.add_non_chapter_question = function () {
        self.non_chapter_questions.push(new TestNonChapterQuestion());
    };

    self.remove_non_chapter_question = function (nonchapter_question) {
        if (nonchapter_question.id()) {
            self.test_questions_to_delete.push(nonchapter_question.id());
        }
        self.non_chapter_questions.remove(nonchapter_question)
    };

    self.validation = function () {
        var valid = true;
        ko.utils.arrayForEach(self.non_chapter_questions(), function (non_chapter_question) {
            if (non_chapter_question.question().type() == 'OBJECTIVE') {
                var has_no_correct_choice = true;
                ko.utils.arrayForEach(non_chapter_question.question().choices(), function (choice) {
                    if (choice.is_correct()) {
                        has_no_correct_choice = false;
                    }
                });
                if (has_no_correct_choice) {
                    valid = false;
                    non_chapter_question.question().errors.push('Atleast one correct choice needed.');
                } else {
                    non_chapter_question.question().errors([]);
                }
            }

        });
        return valid
    };

    self.save = function () {
        if (self.validation()) {
            // App.showProcessing();
            var payload = ko.toJSON(self);
            // var payload = ko.toJS(self);
            console.log(payload);
            if (self.id()){
                var url = '/academy/test/update/' + String(self.id()) + '/';
            }else{
                var url = '/api/test/';
            }


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
            App.remotePost(url, payload, defaultCallback, failureCallback);
        }
    };

}