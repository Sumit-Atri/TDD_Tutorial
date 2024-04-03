from django.test import TestCase
from django.http import HttpRequest
from polls.views import home_page


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