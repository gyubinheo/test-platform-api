from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnswerViewSet, ExplanationViewSet, ProblemViewSet, CategoryListView

app_name = "problems"

router = DefaultRouter()
router.register(r"answers", AnswerViewSet)
router.register(r"explanations", ExplanationViewSet)
router.register(r"problems", ProblemViewSet)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("", include(router.urls)),
]
