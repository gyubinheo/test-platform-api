from django.core.cache import cache
from django.db.models import Count, Q
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
            cache.set("problems", problems, 60 * 60 * 24)
        q = Q()
        solved = self.request.query_params.get("solved")
        difficulty = self.request.query_params.get("difficulty")
        if solved == "false":
            q &= ~Q(submission__result__score=100)
        if difficulty:
            difficulty_values = difficulty.split(",")
            q &= Q(difficulty__in=difficulty_values)
        serializer = ProblemListSerializer(problems.filter(q), many=True)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ExplanationViewSet(viewsets.ModelViewSet):
    queryset = Explanation.objects.all()
    serializer_class = ExplanationSerializer
