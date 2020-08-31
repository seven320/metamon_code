
# class UserTest(TestCase):
#     def setUp(self):
#         User.objects.create(
#             user_name = "電電",
#             user_id = 99,
#             screen_name = "yosyuaomenw",
#             secret_status = "0"
#         )

#         User.objects.create(
#             user_name = "お天気ポワルン",
#             user_id = 199999,
#             screen_name = "systeminfodend1",
#             secret_status = "1"
#         )

#     def test_user_get(self):
#         user = User.objects.get(user_id = 99)
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .serializer import UserSerializer


client = Client()

class GetAllUserTest(TestCase):
    def setUp(self):
        User.objects.create(
            user_name = "電電",
            user_id = 99,
            screen_name = "yosyuaomenw",
            secret_status = "0"
        )

        User.objects.create(
            user_name = "お天気ポワルン",
            user_id = 199999,
            screen_name = "systeminfodend1",
            secret_status = "1"
        )

    def test_get_all_user(self):
        response = client.get('/api/users/')
        user = User.objects.all()
        serializer = UserSerializer(user, many = True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user_with_exist(self):
        fake_user_id = 99
        response = client.get('/api/users/{}/'.format(fake_user_id))
        user = User.objects.get(user_id = fake_user_id)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user_with_non_exist(self):
        fake_user_id = 0
        response = client.get('/api/users/{}/'.format(fake_user_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewUserTest(TestCase):
    def setUp(self):
        self.valid_user = {
            "user_name": "ホゲホゲ",
            "user_id":"12",
            "screen_name":"hogehoge",
            "secret_status":"1"
        }

        self.invalid_user = {
            "user_name": "ホゲホゲ",
            "user_id":"12"
        }

    def test_create_valid_user(self):
        response = client.post(
            "/api/users/",
            data = json.dumps(self.valid_user),
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user(self):
        response = client.post(
            "/api/users/",
            data = json.dumps(self.invalid_user),
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

