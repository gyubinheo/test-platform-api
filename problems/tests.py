from django.core.cache import cache
from django.test import TestCase
from accounts.models import CustomUser
from .models import Category, Problem, Answer, Explanation


class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name=Category.CategoryChoice.STACK_QUEUE)
        Category.objects.create(name=Category.CategoryChoice.BRUTE_FORCE)
        Category.objects.create(name=Category.CategoryChoice.GRAPH_SEARCH)
        Category.objects.create(name=Category.CategoryChoice.DYNAMIC_PROGRAMMING)

    def test_category_name(self):
        stack_queue = Category.objects.get(name="stack_queue")
        brute_force = Category.objects.get(name="brute_force")
        graph_search = Category.objects.get(name="graph_search")
        dynamic_programming = Category.objects.get(name="dynamic_programming")

        self.assertEqual(str(stack_queue), "스택&큐")
        self.assertEqual(str(brute_force), "완전 탐색")
        self.assertEqual(str(graph_search), "그래프 탐색")
        self.assertEqual(str(dynamic_programming), "동적 계획법")

    def test_category_uniqueness(self):
        with self.assertRaises(Exception):
            Category.objects.create(name=Category.CategoryChoice.STACK_QUEUE)


class ProblemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=Category.CategoryChoice.STACK_QUEUE)
        self.user = CustomUser.objects.create_user(email="test@gmali.com", password="testpass")
        self.problem = Problem.objects.create(
            category=self.category,
            difficulty=Problem.Difficulty.EASY,
            title="Test Problem",
            description="Test Problem Description",
            created_by=self.user,
        )

    def test_get_answer_with_cache(self):
        answer = Answer.objects.create(problem=self.problem, code="Test Answer Code")
        cache_key = f"answer_for_problem_{self.problem.pk}"
        cache.set(cache_key, answer, 60)
        self.assertEqual(self.problem.get_answer(), answer.code)

    def test_get_answer_without_cache(self):
        answer = Answer.objects.create(problem=self.problem, code="Test Answer Code")
        self.assertEqual(self.problem.get_answer(), answer.code)

    def test_get_answer_with_missing_answer_object(self):
        self.assertEqual(self.problem.get_answer(), None)

    def test_get_explanation_with_cache(self):
        explanation = Explanation.objects.create(
            problem=self.problem, description="Test Explanation Description"
        )
        cache_key = f"explanation_for_problem_{self.problem.pk}"
        cache.set(cache_key, explanation, 60)
        self.assertEqual(self.problem.get_explanation(), explanation.description)

    def test_get_explanation_without_cache(self):
        explanation = Explanation.objects.create(
            problem=self.problem, description="Test Explanation Description"
        )
        self.assertEqual(self.problem.get_explanation(), explanation.description)

    def test_get_explanation_with_missing_explanation_object(self):
        self.assertEqual(self.problem.get_explanation(), None)

    def test_cache_keys_are_deleted_on_save_and_delete(self):
        answer = Answer.objects.create(problem=self.problem, code="Test Answer Code")
        explanation = Explanation.objects.create(
            problem=self.problem, description="Test Explanation Description"
        )
        cache.set("problems", [self.problem.pk], 60)
        cache.set(f"answer_for_problem_{self.problem.pk}", answer, 60)
        cache.set(f"explanation_for_problem_{self.problem.pk}", explanation, 60)
        answer.save()
        explanation.save()
        self.assertIn(self.problem.pk, cache.get("problems"))
        self.assertIsNone(cache.get(f"answer_for_problem_{self.problem.pk}"))
        self.assertIsNone(cache.get(f"explanation_for_problem_{self.problem.pk}"))
        answer.delete()
        explanation.delete()
        self.assertIn(self.problem.pk, cache.get("problems"))
        self.assertIsNone(cache.get(f"answer_for_problem_{self.problem.pk}"))
        self.assertIsNone(cache.get(f"explanation_for_problem_{self.problem.pk}"))

    def tearDown(self):
        cache.clear()
