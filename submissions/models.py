from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from problems.models import Problem


class Submission(TimeStampedModel):
    class Language(models.TextChoices):
        PYTHON = "python", "Python"
        JAVA = "java", "Java"
        JAVASCRIPT = "javascript", "JavaScript"
        C = "c", "C"
        CPP = "cpp", "C++"

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=10, choices=Language.choices)
    code = models.TextField()

    def __str__(self):
        return f"{self.user.email} submitted {self.problem.title}"


class Result(TimeStampedModel):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    time_taken = models.FloatField()
    memory_used = models.FloatField()
    message = models.TextField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Result for {self.submission.problem.title}"
