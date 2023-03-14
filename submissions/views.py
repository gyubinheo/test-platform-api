from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Submission, Result
from .serializers import SubmissionSerializer
from .tasks import score_submission


class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        score_submission.delay(submission.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmissionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class ResultView(APIView):
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id, user=request.user)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = Result.objects.get(submission=submission)
        except Result.DoesNotExist:
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"score": result.score})
