function Choice() {
    var self = this;
    self.id = ko.observable();
    self.detail = ko.observable();
    self.is_correct = ko.observable(false);

}

// fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')
function Question() {
    var self = this;
    self.true_false_answer_choice = [
        {
            id: true,
            name: 'True'
        },
        {
            id: false,
            name: 'False'
        }
    ];
    self.id = ko.observable();
    self.detail = ko.observable();
    // self.image = ko.observable();
    self.image = ko.observable();
    self.true_false_answer = ko.observable(false);
    self.type = ko.observable();
    self.choices = ko.observableArray(); // points to Choice() type objects
}


function TestQuestion() {
    var self = this;
    self.id = ko.observable();
    self.question = ko.observable(); // points to Question() type object
    self.points = ko.observable();
    self.duration = ko.observable();
}


function TestQuestionAnswer() {
    var self = this;
    self.id = ko.observable();
    self.student = ko.observable();
    self.test_question = ko.observable(); // Points to TestQuestion() type object
    self.true_false_answer = ko.observable();
    self.option_answers = ko.observableArray();
    self.essay_answer_content = ko.observable();
    self.points = ko.observable();

    self.submit = function () {
        var defaultCallback = function (response) {
            if (response.success) {
                App.hideProcessing();
                App.notifyUser('Succesfully Saved', 'success');
                windows.location = '/academy/test/list';
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
        if (!test_question().id()) {
            App.remotePost(url, data, defaultCallback, failureCallback)
        } else {
            console.log('this is chapter question')
        }
    }

}


function Quiz() {
    var self = this;
    self.test_question_answers = ko.observableArray(); // points to TestQuestionAnswer() type objects

    self.previous_question = function () {
        $('.carousel').carousel('prev')
    };
    self.next_question = function () {
        $('.carousel').carousel('next')
    }
}