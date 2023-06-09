from django.conf import settings
from django.core.cache import cache
from django.db import models

from core.models import TimeStampedModel


class Category(TimeStampedModel):
    class CategoryChoice(models.TextChoices):
        STACK_QUEUE = "stack_queue", "스택&큐"
        BRUTE_FORCE = "brute_force", "완전 탐색"
        GRAPH_SEARCH = "graph_search", "그래프 탐색"
        DYNAMIC_PROGRAMMING = "dynamic_programming", "동적 계획법"

    name = models.CharField(max_length=50, choices=CategoryChoice.choices, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        db_table = "categories"


class Problem(TimeStampedModel):
    class Difficulty(models.TextChoices):
        EASY = "1", "쉬움"
        MEDIUM = "2", "보통"
        HARD = "3", "어려움"

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_answer(self):
        cache_key = f"answer_for_problem_{self.pk}"
        answer = cache.get(cache_key)
        if answer:
            return answer.code

        try:
            answer = self.answer
            cache.set(cache_key, answer, 60 * 60 * 24)
            return answer.code
        except Answer.DoesNotExist:
            return None

    def get_explanation(self):
        cache_key = f"explanation_for_problem_{self.pk}"
        explanation = cache.get(cache_key)
        if explanation:
            return explanation.description

        try:
            explanation = self.explanation
            cache.set(cache_key, explanation, 60 * 60 * 24)
            return explanation.description
        except Explanation.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("problems")
        cache.delete(f"answer_for_problem_{self.pk}")
        cache.delete(f"explanation_for_problem_{self.pk}")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("problems")
        cache.delete(f"answer_for_problem_{self.pk}")
        cache.delete(f"explanation_for_problem_{self.pk}")

    class Meta:
        db_table = "problems"


class Answer(TimeStampedModel):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    code = models.TextField()

    def __str__(self):
        return f"Answer for {self.problem.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache_key = f"answer_for_problem_{self.problem.pk}"
        cache.delete(cache_key)

    def delete(self, *args, **kwargs):
        problem_id = self.problem_id
        super().delete(*args, **kwargs)
        cache_key = f"answer_for_problem_{problem_id}"
        cache.delete(cache_key)


class Explanation(TimeStampedModel):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Explanation for {self.problem.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache_key = f"explanation_for_problem_{self.problem.pk}"
        cache.delete(cache_key)

    def delete(self, *args, **kwargs):
        problem_id = self.problem_id
        super().delete(*args, **kwargs)
        cache_key = f"explanation_for_problem_{problem_id}"
        cache.delete(cache_key)
