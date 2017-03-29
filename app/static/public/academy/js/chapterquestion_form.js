// fields = ('id', 'detail', 'is_correct')
function Choice(){
    var self = this;
    self.id = ko.observable();
    self.detail = ko.observable();
    self.is_correct = ko.observable();
    
}

// fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')
function Question(){
    var self = this;

    self.id = ko.observable();
    self.detail = ko.observable();
    self.image = ko.observable();
    self.true_false_answer = ko.observable();
    self.type = ko.observable();
    self.choices = ko.observableArray();

    self.type.subscribe(function(){
        console.log(self.type());
        if(self.type() == 'TRUE/FALSE' || self.type() == 'ESSAY'){
            self.true_false_answer(false);
            self.choices([]);
        }
        if(self.type() == 'OBJECTIVE'){
            self.choices.push(new Choice());
            self.true_false_answer(false);
            console.log(self.true_false_answer());
        }

    });

    self.add_choice = function(){
        self.choices.push(new Choice())
    };
}

function ChapterQuestion(chapter_id){
    var self = this;
    self.chapter_id = ko.observable(chapter_id);
    self.questions = ko.observableArray([new Question()]);

    self.add_question = function(){
        self.questions.push(new Question());
    };

    self.save = function(){
        var payload = JSON.parse(ko.toJSON(self));
        console.log(payload);
    };


}