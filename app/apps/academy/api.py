import json

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

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


class TestViewset(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = json.loads(request.data)
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(data={}, status=201)
        else:
            return Response(data=serializer.errors, status=406)

    def update(self, request, *args, **kwargs):
        data = json.loads(request.data)

        # Delete Removed
        # TODO update test question to delete from js
        TestQuestion.objects.filter(id__in=data.get('test_questions_to_delete')).delete()
        for test_question in data.get('non_chapter_questions'):
            choices_to_delete = test_question.get('question').get('choices_to_delete')
            Option.objects.filter(id__in=choices_to_delete)

        test_id = kwargs.get('pk')
        test_obj = Test.objects.get(id=test_id)
        serializer = TestSerializer(test_obj, data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(data={}, status=201)
        else:
            return Response(data=serializer.errors, status=406)
        pass