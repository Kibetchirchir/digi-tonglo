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

        self.user1 = User.objects.create_user(username='test', email='test@test.com', password='eser3456', phone_number='test')

    def test_user_saved(self):
        """User is saved on the db"""
        self.assertEqual(str(self.user1), 'test@test.com')

    def test_user_without_username(self):
        """
        test if User can be saved without username
        :return:
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(None, self.user["email"], phone_number='yesdy')

        self.assertEqual(str(error_message.exception), 'Users must have a username.')

    def test_user_without_email(self):
        """
        test user can be saved without email
        :return:
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(self.user["username"], None, phone_number='dfsdfsdfdsfdsf')

        self.assertEqual(str(error_message.exception), 'Users must have an email address.')

    def test_register_user_2(self):
        """
        test error if user is registered twice
        :return:
        """
        # test = self.user1
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='test', email='test@test.com', password='eser3456', phone_number='test')


class UserTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # add test data
        self.user = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "079215135421",
                "phone_number": "0792151354"
            }
        }

        self.user_254 = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "079215135421",
                "phone_number": "254792151354"
            }
        }

        self.user_wrong_number = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "079215135421",
                "phone_number": "9215135421"
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

    def test_wrong_phone_number_validate(self):
        """
        test user with a number with error
        :return:
        """
        response = self.client.post('/api/users/', self.user_wrong_number, format='json')
        result = json.loads(response.content)
        self.assertEqual(result["phone_number"], ["The phone number is should start with 07 or 254(the code)"])
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


class UserLogin(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "079215135421",
                "phone_number": "079215135421"
            }
        }

        self.wrong_user = {
            "user": {
                "email": "chirchir@gmail.com",
                "username": "vokechi",
                "password": "0792155421",
                "phone_number": "079215135421"
            }
        }

        self.client.post('/api/users/', self.user, format='json')

    def test_login_user(self):
        response = self.client.post('/api/users/login/', self.user, format='json')
        result = json.loads(response.content)
        self.assertEqual(result["email"], "chirchir@gmail.com")

    def test_wrong_credentials(self):
        response = self.client.post('/api/users/login/', self.wrong_user, format='json')
        result = json.loads(response.content)

        self.assertEqual(result["non_field_errors"], ["Invalid email or password provided."])
