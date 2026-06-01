import os
from http.client import responses
from itertools import count

import django
from django.urls import reverse
from rest_framework import status

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.conf import settings
from rest_framework.test import APITestCase
from users.models import User


class LessonsTestCase(APITestCase):

    id_lesson = 0

    def setUp(self):
        """Выполняется перед каждым тестом: готовим данные."""
        super().setUp()
        self.user = User.objects.create(
            email="test@test.com",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create_wrong(self):
        url = reverse("lms:lesson_create")
        response = self.client.post(
            url, data={"name": "Test Lesson", "url_video": "Test lesson"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        response = self.client.post(
            url, data={"name": "Test Lesson", "url_video": "https://youtube.com"}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], "Test Lesson")
        self.id_lesson = data["id"]

    def test_lesson_retrieve(self):
        self.test_lesson_create()
        url = reverse("lms:lesson_retrieve", kwargs={"pk": self.id_lesson})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        self.test_lesson_create()
        url = reverse("lms:lesson_update", kwargs={"pk": self.id_lesson})
        response = self.client.put(
            url, data={"name": "Test Lesson2", "url_video": "https://youtube.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Test Lesson2")

    def test_lesson_destroy(self):
        self.test_lesson_create()
        url = reverse("lms:lesson_destroy", kwargs={"pk": self.id_lesson})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        self.test_lesson_create()
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        data = response.json()
        self.assertTrue(data.get("count") >= 1)
        self.assertTrue(len(data.get("results")) >= 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
