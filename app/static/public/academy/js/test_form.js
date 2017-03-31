// fields = ('id', 'detail', 'is_correct')
function Choice() {
    var self = this;
    self.id = ko.observable();
    self.detail = ko.observable();
    self.is_correct = ko.observable(false);

}

function ChapterQuestion() {
    var self = this;
    self.question_id = ko.observable();
    self.points = ko.observable();
}

// fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')
function NewQuestion() {
    var self = this;

    self.id = ko.observable();
    self.points = ko.observable();
    self.detail = ko.observable();
    // self.image = ko.observable();
    self.image = ko.observable({
        dataURL: ko.observable()
    });
    self.true_false_answer = ko.observable(false);
    self.type = ko.observable();
    self.choices = ko.observableArray();
    self.errors = ko.observableArray();
    // self.question_error_class = ko.observable();

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
    self.course = ko.observable();
    self.pass_marks = ko.observable();
    self.pass_marks = ko.observable();
    self.questions = ko.observable();

    self.add_question = function () {
        self.questions.push(new Question());
    };

    self.remove_question = function (question) {
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