from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import ChapterPage, Question
from .serializers import QuestionSerializer


class ChapterQuestionViewSet(viewsets.ViewSet):

    @detail_route(methods=['get'], permission_classes=[])
    def chapterquestions_list(self, request, pk):
        queryset = ChapterPage.objects.get(id=pk).questions.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], permission_classes=[])
    def chapterquestions_update(self,request, pk):
        pass


