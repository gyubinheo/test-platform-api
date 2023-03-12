from rest_framework import serializers
from .models import Category, Problem, Answer, Explanation


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="get_name_display")

    class Meta:
        model = Category
        fields = ["id", "category_name"]


class ProblemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.get_name_display")
    created_user_email = serializers.CharField(source="created_by.email")

    class Meta:
        model = Problem
        fields = [
            "id",
            "category_name",
            "title",
            "description",
            "difficulty",
            "created_user_email",
            "answer",
            "explanation",
            "updated_at",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "problem", "code"]


class ExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ["id", "problem", "description"]