from django.test import TestCase, Client
from django.http import HttpRequest

from polls.models import Item, List
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


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, mylist)

class TodoPageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("http://127.0.0.1:8000/polls/todo/")
        self.assertTemplateUsed(response, "todo.html")

    def test_only_saves_items_when_necessary(self):
        self.client.get("http://127.0.0.1:8000/polls/todo/")
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"http://127.0.0.1:8000/polls/todo/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "lists.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"http://127.0.0.1:8000/polls/todo/lists/{correct_list.id}/")

        print(response.content)

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"http://127.0.0.1:8000/polls/todo/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"http://127.0.0.1:8000/polls/todo/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"http://127.0.0.1:8000/polls/todo/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"http://127.0.0.1:8000/polls/todo/lists/{correct_list.id}/", fetch_redirect_response=False)