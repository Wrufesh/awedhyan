from django.utils.regex_helper import Choice
from rest_framework import serializers

from .models import Test, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'detail', 'question', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'detail', 'image', 'true_false_answer', 'type', 'choices')


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'course', 'pass_mark', 'questions')
