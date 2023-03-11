from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Category(TimeStampedModel):
    class CategoryChoice(models.TextChoices):
        STACK_QUEUE = "stack_queue", "스택&큐"
        BRUTE_FORCE = "brute_force", "완전 탐색"
        GRAPH_SEARCH = "graph_search", "그래프 탐색"
        DYNAMIC_PROGRAMMING = "dynamic_programming", "동적 계획법"

    name = models.CharField(max_length=50, choices=CategoryChoice.choices)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        db_table = "categories"


class Problem(TimeStampedModel):
    class Difficulty(models.TextChoices):
        EASY = "easy", "쉬움"
        MEDIUM = "medium", "보통"
        HARD = "hard", "어려움"

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "problems"


class TestCase(TimeStampedModel):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()

    def __str__(self):
        return f"Testcase for {self.problem.title}"
