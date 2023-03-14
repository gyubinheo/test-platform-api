from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.SubmissionListCreateView.as_view()),
    path("api/<int:pk>/", views.SubmissionRetrieveUpdateDestroyView.as_view()),
    path("api/<int:submission_id>/result/", views.ResultView.as_view()),
]
