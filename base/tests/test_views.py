from unittest import skip
from django.test import TestCase,Client
from django.urls import reverse
from django.http import HttpRequest
#
from base.models import User,Room,Topic
from base.views import home


@skip("demonstrating skip")
class TestSkip(TestCase):
    def test_skip_example():
        pass

class TestViewResponses(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.c = Client()
        # setup the database
        User.objects.create(username='admin',email='admin@admin.com')
        Topic.objects.create(name='Coding')
        Room.objects.create(name='test',host_id=1,topic_id=1)
    
    def test_url_allowed_hosts(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code,200)

    def test_room_detail_url(self):
        response = self.c.get(reverse('room',args=['test']))
        self.assertEqual(response.status_code,200)
        #
        response = self.c.get(reverse('room',args=['test-django']))
        self.assertEqual(response.status_code,404)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        response = home(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>StudyBuddy - Find study partners around the world!</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
