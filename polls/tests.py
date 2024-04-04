from django.test import TestCase, Client
from django.http import HttpRequest

from polls.models import Item
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


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")

class TodoPageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("http://127.0.0.1:8000/polls/todo/")
        self.assertTemplateUsed(response, "todo.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")
        response = self.client.get("http://127.0.0.1:8000/polls/todo/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_can_save_a_POST_request(self):
        self.client.post("http://127.0.0.1:8000/polls/todo/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("http://127.0.0.1:8000/polls/todo/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "http://127.0.0.1:8000/polls/todo/", fetch_redirect_response=False)

    def test_only_saves_items_when_necessary(self):
        self.client.get("http://127.0.0.1:8000/polls/todo/")
        self.assertEqual(Item.objects.count(), 0)