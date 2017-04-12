import json

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from app.utils.utilities import base64_content_file
from .models import ChapterPage, Question, Test, TestQuestion, Option
from .serializers import QuestionSerializer, ChapterPageSerializer, TestSerializer


# class ChapterQuestionViewSet(viewsets.ViewSet):
#
#     @detail_route(methods=['get'], permission_classes=[])
#     def chapterquestions_list(self, request, pk):
#         queryset = ChapterPage.objects.get(id=pk).questions.all()
#         serializer = QuestionSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @detail_route(methods=['post'], permission_classes=[])
#     def chapterquestions_update(self,request, pk):
#         pass
#

class CourseChapterPageViewset(viewsets.ModelViewSet):
    queryset = ChapterPage.objects.all()
    serializer_class = ChapterPageSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = ChapterPage.objects.all()
        course_id = self.request.query_params.get('course_id', None)
        if course_id:
            queryset = queryset.filter(course__id=course_id)
        return queryset


class TestQuestionAnswerViewset():
    pass