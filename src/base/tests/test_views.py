from unittest import skip

# from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from base.models import Room, Topic, User

# from base.views import home
from http import HTTPStatus

# Import the modules you need
# Import the modules you need
# from django.urls import resolve
from base import views
import inspect  # Import the inspect module to check the source of the functions

# Import the modules you need
from django_extensions.management.commands.show_urls import Command as ShowUrlsCommand
import json

# Define a test case class
from base.urls import urlpatterns


class ViewTestCase(TestCase):
    def get_all_base_urls(self):
        # Create an instance of the show_urls command
        show_urls = ShowUrlsCommand()
        # Call the handle method with the desired arguments
        # For example, you can pass the app name to filter the urls by app
        output = show_urls.handle(
            appname="base",
            no_color=True,
            language="en",
            decorator="",
            unsorted="",
            format_style="json",
            urlconf="ROOT_URLCONF_BASE",
            traceback="",
        )

        output_list = json.loads(output)

        return output_list

    # Define a helper method to get all the view functions in views.py
    def get_view_functions(self):
        # Get all the attributes of the views module
        attrs = dir(views)
        # Filter out the ones that start with underscore or are not callable
        funcs = [getattr(views, attr) for attr in attrs if not attr.startswith("_") and callable(getattr(views, attr))]
        # Filter out the ones that are imported from other modules
        funcs = [
            func for func in funcs if inspect.getmodule(func) == views
        ]  # Check if the function's module is the same as the views module
        # Return the list of functions
        return funcs

    # Define a test method to check if all the view functions are used in urls
    def test_view_functions_are_used_in_urls(self):
        # Get all the view functions
        view_funcs = self.get_view_functions()
        view_urls = urlpatterns

        # Loop through each function
        for func in view_funcs:
            found = False
            for url in view_urls:
                if func is url.callback:
                    found = True
                    break

            if not found:
                self.fail(f"{func.__name__} is not used in urls")


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


@skip("demonstrating skip 2")
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
        # response = self.c.get(reverse("home"))
        # self.assertEqual(response.status_code, 200)
        # self.assertIn("<title>StudyBuddy - Find study partners around the world!</title>", response.content)
        # self.assertTrue(response.content.find("\n<!DOCTYPE html>\n"))

    def test_url_allowed_hosts_2(self):
        response = self.c.get("/", HTTP_HOST="noaddresss.com")
        self.assertEqual(response.status_code, 400)
