# Generated by Django 3.2.25 on 2024-11-30 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20241130_0532"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Ingredients",
            new_name="Ingredient",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="ingredients",
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredient",
            field=models.ManyToManyField(to="core.Ingredient"),
        ),
    ]
