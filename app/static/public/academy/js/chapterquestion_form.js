// fields = ('id', 'detail', 'is_correct')
function Choice() {
    var self = this;
    self.id = ko.observable();
    self.detail = ko.observable();
    self.is_correct = ko.observable(false);

}

// fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')
function Question() {
    var self = this;

    self.id = ko.observable();
    self.detail = ko.observable();
    self.image = ko.observable();
    self.true_false_answer = ko.observable(false);
    self.type = ko.observable();
    self.choices = ko.observableArray();

    self.choices_to_delete = ko.observableArray();

    self.type.subscribe(function () {
        console.log(self.type());
        if (self.type() == 'TRUE/FALSE' || self.type() == 'ESSAY') {
            self.true_false_answer(false);
            self.choices([]);
        }
        if (self.type() == 'OBJECTIVE') {
            self.choices.push(new Choice());
            self.true_false_answer(false);
            console.log(self.true_false_answer());
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
}

function ChapterQuestion(chapter_id) {
    var self = this;
    self.chapter_id = ko.observable(chapter_id);
    self.questions = ko.observableArray([new Question()]);

    self.questions_to_delete = ko.observableArray();

    self.add_question = function () {
        self.questions.push(new Question());
    };

    self.remove_question = function (question) {
        if (question.id()) {
            self.questions_to_delete.push(question.id());
        }
        self.questions.remove(question)
    };

    self.save = function () {
        App.showProcessing();
        var payload = JSON.parse(ko.toJSON(self));
        var url = '/academy/chapterquestions/add/' + String(self.chapter_id()) + '/';


        var defaultCallback = function (response) {
            if (response.success) {
                App.hideProcessing();
                App.notifyUser('Succesfully Saved');
            }
        };
        var failureCallback = function (err) {
            var err_message = err.responseJSON.detail;
            var error = App.notifyUser(
                err_message,
                'error'
            );
            App.hideProcessing();
        }
        App.remotePost(url, payload, defaultCallback, failureCallback);
    };


}