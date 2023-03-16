from django.urls import path
from . import views

urlpatterns = [
    path("", views.SubmissionListCreateView.as_view()),
    path("<int:pk>/", views.SubmissionRetrieveUpdateDestroyView.as_view()),
    path("<int:submission_id>/result/", views.ResultView.as_view()),
]
