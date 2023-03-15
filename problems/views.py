from django.core.cache import cache
from django.db.models import Count
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Category, Problem, Answer, Explanation
from .serializers import (
    CategorySerializer,
    ProblemListSerializer,
    ProblemDetailSerializer,
    AnswerSerializer,
    ExplanationSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer

    def list(self, request, *args, **kwargs):
        problems = cache.get("problems")
        if not problems:
            problems = (
                self.get_queryset()
                .annotate(num_submissions=Count("submission"))
                .order_by("difficulty", "num_submissions", "-created_at")
            )
        serializer = ProblemListSerializer(problems, many=True)
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
