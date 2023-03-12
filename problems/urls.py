from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"problems", views.ProblemViewSet)
router.register(r"answers", views.AnswerViewSet)
router.register(r"explanations", views.ExplanationViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/category/", views.CategoryListView.as_view()),
]
