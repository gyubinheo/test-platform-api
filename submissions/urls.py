from django.urls import path
from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.SubmissionListCreateView.as_view(), name="list"),
    path("<int:pk>/", views.SubmissionRetrieveUpdateDestroyView.as_view(), name="detail"),
    path("<int:submission_id>/result/", views.ResultView.as_view(), name="result"),
]
