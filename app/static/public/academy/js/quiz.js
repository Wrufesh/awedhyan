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
    // self.image = ko.observable();
    self.image = ko.observable({
        dataURL: ko.observable()
    });
    self.true_false_answer = ko.observable(false);
    self.type = ko.observable();
    self.choices = ko.observableArray();
}

// function QuizQuestion(){
//     var self = this;
//     // below is test question id
//     self.id = ko.observable();
//     self.question = ko.observable();
//     self.points = ko.observable();
//     self.test = ko.observable();
//     self.student = ko.observable();
// }

function TestQuestion(){
    var self = this;
    self.id = ko.observable();
    self.question = ko.observable();
    self.points = ko.observable();
    self.test = ko.observable();
    self.student = ko.observable();
    self.true_false_answer = ko.observable();
    self.option_answers = ko.observableArray();
    self.essay_answer = ko.observable();
    self.image = ko.observable({
        dataURL: ko.observable()
    });
    self.points = ko.observable();

}


function Quiz(){
    var self = this;
    self.quiz_questions = ko.observableArray();
    self.quiz_answers = ko.observableArray();
}