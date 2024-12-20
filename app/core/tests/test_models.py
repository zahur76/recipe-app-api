"""_
Test for models
"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email"""

        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_email_normalized(self):
        """Test creating normalized email for a user"""

        sample_email = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2.example.com", "Test2.example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(
                email, password="testpassword"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Test creating user without email raises an exception"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpassword")

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            "test@eaxmaple.com", "testpassword"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""

        user = get_user_model().objects.create_user(
            "test@exmaple.com", "testpassword"
        )

        recipe = models.Recipe.objects.create(
            title="Test Recipe",
            user=user,
            price=Decimal("5.50"),
            time_minutes=50,
            description="Sample recipe description",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(name="Sample Tag", user=user)

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            name="Ingredient1",
            user=user,
        )
        self.assertEqual(str(ingredient), ingredient.name)
