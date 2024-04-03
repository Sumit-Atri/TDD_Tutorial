from django.test import TestCase, Client
from django.http import HttpRequest
from polls.views import home_page, get_users
from django.urls import reverse
import json

class HomePageTest(TestCase):
    # Test to check if returning correct HTML
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        # self.assertIn("<title>Question Voting App</title>", html)
        # self.assertTrue(html.startswith("<html>"))
        # self.assertTrue(html.endswith("</html>"))

        self.assertContains(response, "<title>Question Voting App</title>")
        self.assertContains(response, "<h1>Questions</h1>")

    # Test to check if we are calling correct view function at url "/"
    def test_home_page_returns_correct_html_2(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>Question Voting App</title>")

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class UsersAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def users_returns_correct_html(self):
        request = HttpRequest()
        response = get_users(request)
        html = response.content.decode("utf8")
        # self.assertIn("<title>Question Voting App</title>", html)
        # self.assertTrue(html.startswith("<html>"))
        # self.assertTrue(html.endswith("</html>"))

        #self.assertContains(response, "<title>Question Voting App</title>")
        self.assertContains(response, "<h1>User List</h1>")

    # Test to see if we are getting users at desired url
    def test_get_users(self):
        response = self.client.get("http://127.0.0.1:8000/polls/users/")
        self.assertEqual(response.status_code, 200)

    # Test to see if correct template was used.
    def user_template_used(self):
        response = self.client.get("http://127.0.0.1:8000/polls/users/")
        self.assertTemplateUsed(response, "users.html")

    def test_singleuser_detail_correct_html(self):
        response = self.client.get("http://127.0.0.1:8000/polls/users/2/")
        self.assertContains(response, "<title>User Details</title>")


