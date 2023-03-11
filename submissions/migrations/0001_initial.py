# Generated by Django 4.1.7 on 2023-03-11 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("problems", "0002_explanation_answer"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("modified_time", models.DateTimeField(auto_now=True)),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("python", "Python"),
                            ("java", "Java"),
                            ("javascript", "JavaScript"),
                            ("c", "C"),
                            ("cpp", "C++"),
                        ],
                        max_length=10,
                    ),
                ),
                ("code", models.TextField()),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="problems.problem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("modified_time", models.DateTimeField(auto_now=True)),
                ("time_taken", models.FloatField()),
                ("memory_used", models.FloatField()),
                ("message", models.TextField()),
                ("score", models.IntegerField(default=0)),
                (
                    "submission",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submissions.submission",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
