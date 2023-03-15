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

    def update(self, instance, validated_data):
        answer_data = validated_data.pop("answer", None)
        explanation_data = validated_data.pop("explanation", None)

        instance.category = validated_data.get("category", instance.category)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.difficulty = validated_data.get("difficulty", instance.difficulty)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.save()

        if answer_data:
            answer_serializer = self.fields["answer"]
            answer_serializer.update(instance.answer, answer_data)

        if explanation_data:
            explanation_serializer = self.fields["explanation"]
            explanation_serializer.update(instance.explanation, explanation_data)

        return instance

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
