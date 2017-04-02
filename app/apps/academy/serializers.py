from django.utils.regex_helper import Choice
from rest_framework import serializers

from .models import Test, Question, Option, TestQuestion, Course, ChapterPage


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
        model = TestQuestion
        fields = ('id', 'question', 'chapter', 'points')


class ChapterPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterPage
        fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterPageSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'chapters')


class TestSerializer(serializers.ModelSerializer):
    non_chapter_questions = TestQuestionSerializer(source='get_non_chapter_questions', many=True)
    chapter_questions = TestQuestionSerializer(source='get_chapter_questions', many=True)
    # course = CourseSerializer(many=False)

    class Meta:
        model = Test
        fields = ('id', 'name', 'course', 'pass_mark', 'non_chapter_questions', 'chapter_questions')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
