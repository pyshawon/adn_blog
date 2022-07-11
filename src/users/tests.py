from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from users.models import User
from posts.models import Post
from comments.models import Comment


# Create your tests here.

class UsersManagersTests(TestCase):
    """
    Test Custom user manager
    """
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal_user@adn.com', password='adn@adn')
        self.assertEqual(user.email, 'normal_user@adn.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="adn@adn")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super_adn@adn.com', password='adn@adn')
        self.assertEqual(admin_user.email, 'super_adn@adn.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super_adn@adn.com', password='adn@adn', is_superuser=False)


class UserTestCase(TestCase):
    """
    Test Case for User.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="pyshawon.test@gmail.com",
            password="admin@123",
            is_active=True
        )

        self.user1 = User.objects.create_user(
            email="pyshawon.test1@gmail.com",
            password="admin@123",
            is_active=False
        )

    def test_user_login(self):
        """
        Test User Login
        """
        data = {
            "email":"pyshawon.test@gmail.com",
            "password":"admin@123"
        }
        response = self.client.post("/user/login/", data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")





