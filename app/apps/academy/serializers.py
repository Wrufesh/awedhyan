import base64

from django.db import transaction
from django.utils.regex_helper import Choice
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from app.utils.fields import Base64ImageField
from .models import Test, Question, Option, TestQuestion, Course, ChapterPage, TestQuestionAnswer


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
        fields = ('id', 'question', 'points', 'duration')


class TestQuestionMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ('id', 'question', 'chapter', 'points', 'duration')

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


class TestQuestionAnswerSerializer(serializers.ModelSerializer):
    test_question = TestQuestionDetailSerializer(many=False)
    option_answers = ChoiceSerializer(many=True)
    class Meta:
        model = TestQuestionAnswer
        fields = ('id', 'student', 'test_question', 'true_false_answer', 'option_answers', 'essay_answer', 'image', 'points')