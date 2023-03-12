from django.core.cache import cache
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Category, Problem, Answer, Explanation
from .serializers import (
    CategorySerializer,
    ProblemSerializer,
    AnswerSerializer,
    ExplanationSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def list(self, request):
        problems = cache.get("problems")
        if not problems:
            problems = Problem.objects.all()
            cache.set("problems", problems, 60 * 60)
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        problem = self.get_object()
        serializer = self.get_serializer(problem)
        serializer.data["answer"] = problem.get_answer()
        serializer.data["explanation"] = problem.get_explanation()
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ExplanationViewSet(viewsets.ModelViewSet):
    queryset = Explanation.objects.all()
    serializer_class = ExplanationSerializer
