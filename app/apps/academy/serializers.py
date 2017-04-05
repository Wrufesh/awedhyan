import base64
from django.utils.regex_helper import Choice
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from app.utilities import base64_content_file
from .models import Test, Question, Option, TestQuestion, Course, ChapterPage


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'detail', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    image = Base64ImageField(required=False)

    def validate_image(self, value):
        import ipdb
        ipdb.set_trace()
        # if value.get('fileArray', None):
        #     if value.get('dataURL', None):
        #         return value.get('dataURL')
        #     else:
        #         raise serializers.ValidationError("No file data present")
        # else:
        #     return None

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

    # course = CourseSerializer(many=False)

    class Meta:
        model = Test
        fields = ('id', 'name', 'course', 'pass_mark', 'non_chapter_questions', 'chapter_questions')

    # def create(self, validated_data):
    #     test = Test.objects.create(**{
    #         'name': validated_data.get('name'),
    #         'course': validated_data.get('course'),
    #         'pass_mark': validated_data.get('pass_mark')
    #     })
    #     # TODO save non_chapter_questions and chapter questions
    #
    #     return test
    #
    # def update(self, instance, validated_data):
    #     pass
