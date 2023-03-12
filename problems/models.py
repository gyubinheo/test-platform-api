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

    def get_answer(self):
        cache_key = f"answer_for_problem_{self.pk}"
        answer = cache.get(cache_key)
        if answer is not None:
            return answer

        try:
            answer = self.answer
            cache.set(cache_key, answer, timeout=60 * 60)
            return answer
        except Answer.DoesNotExist:
            return None

    def get_explanation(self):
        cache_key = f"explanation_for_problem_{self.pk}"
        explanation = cache.get(cache_key)
        if explanation is not None:
            return explanation

        try:
            explanation = self.explanation
            cache.set(cache_key, explanation, timeout=60 * 60)
            return explanation
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


class TestCase(TimeStampedModel):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()

    def __str__(self):
        return f"Testcase for {self.problem.title}"


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
