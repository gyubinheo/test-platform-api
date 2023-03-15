from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnswerViewSet, ExplanationViewSet, ProblemViewSet, CategoryListView

router = DefaultRouter()
router.register("answers", AnswerViewSet)
router.register("explanations", ExplanationViewSet)
router.register("problems", ProblemViewSet)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("", include(router.urls)),
]
