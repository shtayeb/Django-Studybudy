from unittest import skip

from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from base.models import Room, Topic, User
from base.views import home
from http import HTTPStatus


class RobotsTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "text/plain"
        assert response.content.startswith(b"User-Agent: *\n")

    def test_post_disallowed(self):
        response = self.client.post("/robots.txt")

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@skip("demonstrating skip")
class TestSkip(TestCase):
    def test_skip_example():
        pass


class TestViewResponses(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.c = Client()
        # setup the database
        User.objects.create(username="admin", email="admin@admin.com")
        Topic.objects.create(name="Coding")
        Room.objects.create(name="test", host_id=1, topic_id=1)

    def test_url_allowed_hosts(self):
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_room_detail_url(self):
        response = self.c.get(reverse("room", args=["test"]))
        self.assertEqual(response.status_code, 200)
        #
        response = self.c.get(reverse("room", args=["test-django"]))
        self.assertEqual(response.status_code, 404)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        response = home(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>StudyBuddy - Find study partners around the world!</title>", html)
        self.assertTrue(html.find("\n<!DOCTYPE html>\n"))
        self.assertEqual(response.status_code, 200)

    def test_url_allowed_hosts_2(self):
        response = self.c.get("/", HTTP_HOST="noaddresss.com")
        self.assertEqual(response.status_code, 400)
