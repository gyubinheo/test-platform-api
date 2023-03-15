from rest_framework import serializers
from .models import Category, Problem, Answer, Explanation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "get_name_display"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "problem_id", "code"]


class ExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ["id", "problem_id", "description"]


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id",
            "category",
            "title",
            "get_difficulty_display",
        ]


class ProblemDetailSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    explanation = ExplanationSerializer()

    def create(self, validated_data):
        answer_data = validated_data.pop("answer")
        explanation_data = validated_data.pop("explanation")
        problem = Problem.objects.create(**validated_data)
        Answer.objects.create(problem=problem, **answer_data)
        Explanation.objects.create(problem=problem, **explanation_data)
        return problem

    class Meta:
        model = Problem
        fields = [
            "id",
            "category",
            "title",
            "description",
            "difficulty",
            "created_by",
            "updated_at",
            "answer",
            "explanation",
        ]
