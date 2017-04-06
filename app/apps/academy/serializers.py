import base64

from django.db import transaction
from django.utils.regex_helper import Choice
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from app.utils.fields import Base64ImageField
from .models import Test, Question, Option, TestQuestion, Course, ChapterPage


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'detail', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Question
        fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')


class TestQuestionDetailSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = TestQuestion
        fields = ('id', 'question', 'points')


class TestQuestionMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ('id', 'question', 'chapter', 'points')

    def create(self, validated_data):
        TestQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class ChapterPageSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = ChapterPage
        fields = ('id', 'name', 'questions')


class TestSerializer(serializers.ModelSerializer):
    non_chapter_questions = TestQuestionDetailSerializer(source='get_non_chapter_questions', many=True)
    chapter_questions = TestQuestionMinSerializer(source='get_chapter_questions', many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'course', 'pass_mark', 'non_chapter_questions', 'chapter_questions')

    def create(self, validated_data):

        with transaction.atomic():
            test = Test.objects.create(**{
                'name': validated_data.get('name'),
                'course': validated_data.get('course'),
                'pass_mark': validated_data.get('pass_mark'),
                'created_by': validated_data.get('created_by')
            })

            test_questions = []
            for chapter_question in validated_data['get_chapter_questions']:
                test_questions.append(TestQuestion.objects.create(**chapter_question))
            for non_chapter_question in validated_data['get_non_chapter_questions']:
                question_obj_data = non_chapter_question.pop('question')
                choices_data = question_obj_data.pop('choices')
                question_obj = Question.objects.create(**question_obj_data)
                for choice_data in choices_data:
                    Option.objects.create(question=question_obj, **choice_data)
                test_questions.append(
                    TestQuestion.objects.create(
                        question=question_obj,
                        points=non_chapter_question.get('points')
                    )
                )
            test.questions.add(*test_questions)

        return test

    def update(self, instance, validated_data):
        import ipdb
        ipdb.set_trace()
        # with transaction.atomic():
        #     instance.name = validated_data.get('name')
        #     instance.course = validated_data.get('course')
        #     instance.pass_mark = validated_data.get('pass_mark')
        #     instance.save()
        #
        #     test_questions = []
        #     for chapter_question in validated_data['get_chapter_questions']:
        #         ch_ques_obj, created = TestQuestion.objects.update_or_create(id=chapter_question.pop('id'),
        #                                                                      defaults=chapter_question)
        #         if created:
        #             test_questions.append(ch_ques_obj)
        #
        #     for non_chapter_question in validated_data['get_non_chapter_questions']:
        #         question_obj_data = non_chapter_question.pop('question')
        #         choices_data = question_obj_data.pop('choices')
        #         question_obj, created = Question.objects.update_or_create(id=question_obj_data.pop('id'),
        #                                                                   defaults=question_obj_data)
        #         for choice_data in choices_data:
        #             choices_data['question'] = question_obj
        #             option_obj, created = Option.objects.update_or_create(id=choices_data.pop('id'),
        #                                                                   defaults=choice_data)
        #
        #         non_chapter_question['question'] = question_obj
        #         non_ch_ques_obj, created = TestQuestion.objects.update_or_create(id=non_chapter_question.pop('id'),
        #                                                                          defaults=non_chapter_question)
        #         if created:
        #             test_questions.append(
        #                 non_ch_ques_obj
        #             )
        #     instance.questions.add(*test_questions)
        #
        # return instance
