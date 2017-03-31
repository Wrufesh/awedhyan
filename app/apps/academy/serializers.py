from django.utils.regex_helper import Choice
from rest_framework import serializers

from .models import Test, Question, Option, TestQuestion


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'detail', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')


class TestQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)
    class Meta:
        models = TestQuestion
        fields = ('id', 'question', 'points')


class TestSerializer(serializers.ModelSerializer):
    questions = TestQuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'course', 'pass_mark', 'questions')
