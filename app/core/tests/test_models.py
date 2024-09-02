"""_
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email"""

        email = 'test@example.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_email_normalized(self):
        """Test creating normalized email for a user"""

        sample_email = [['test1@EXAMPLE.com', 'test1@example.com'],
                        ['Test2.example.com', 'Test2.example.com'],
                        ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
                        ['test4@example.COM', 'test4@example.com']]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(
                email, password='testpassword')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Test creating user without email raises an exception"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpassword')

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            'test@eaxmaple.com', 'testpassword')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
