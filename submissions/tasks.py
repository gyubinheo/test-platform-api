from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import Submission, Result


@shared_task
def score_submission(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        problem = submission.problem
        if submission.code == problem.answer.code:
            score = 100
        else:
            score = 0
        Result.objects.create(submission=submission, score=score)
        return f"Scored submission {submission_id}, score={score}"
    except ObjectDoesNotExist:
        return f"Submission {submission_id} not found"
