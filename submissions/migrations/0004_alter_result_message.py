# Generated by Django 4.1.7 on 2023-03-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0003_remove_result_memory_used_remove_result_time_taken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="message",
            field=models.TextField(blank=True),
        ),
    ]