from django.test import TestCase
from .models import User
from django.db import IntegrityError
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class UserManagerTestCase(TestCase):

    def setUp(self):
        self.user = {
            "email": "bae@email.com",
            "username": "bae",
            "password": "071232445"
        }

        self.user1 = User.objects.create_user(username='test', email='test@test.com', password='eser3456')

    def test_user_saved(self):
        """User is saved on the db"""
        self.assertEqual(str(self.user1), 'test@test.com')

    def test_user_without_username(self):
        """
        test if User can be saved without username
        :return:
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(None, self.user["email"])

        self.assertEqual(str(error_message.exception), 'Users must have a username.')

    def test_user_without_email(self):
        """
        test user can be saved without email
        :return:
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(self.user["username"], None)

        self.assertEqual(str(error_message.exception), 'Users must have an email address.')

    def test_register_user_2(self):
        """
        test error if user is registered twice
        :return:
        """
        # test = self.user1
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='test', email='test@test.com', password='eser3456')


class UserTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # add test data
        self.user = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "07921513542"
            }
        }

    def test_register_user(self):
        """
        test register
        """
        # hit the API endpoint
        response = self.client.post('/api/users/', self.user, format='json')
        result = json.loads(response.content)
        self.assertEqual(result["email"], "chirchir@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

