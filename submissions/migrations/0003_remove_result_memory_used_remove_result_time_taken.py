# Generated by Django 4.1.7 on 2023-03-14 12:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0002_rename_created_time_result_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="memory_used",
        ),
        migrations.RemoveField(
            model_name="result",
            name="time_taken",
        ),
    ]
