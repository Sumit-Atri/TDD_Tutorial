import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

import json

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # def test_can_start_a_pollsapp(self):
    #     # Edith has heard about a cool new online poll app.
    #     # She goes to check out its homepage
    #     self.browser.get("http://localhost:8000")
    #
    #     # She notices the page title and header mention to-do lists
    #     self.assertIn("Polls", self.browser.title)
    #
    #     # She is invited to enter a to-do item straight away
    #     self.fail("Finish the test!")
    #
    #     [...]

        # Satisfied, she goes back to sleep

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                print(self.browser)
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
    def test_can_vote_on_question(self):
        # User opens the app
        self.browser.get("http://localhost:8000")

        # User sees a set of questions
        self.assertIn("Question Voting App", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Questions", header_text)

        # User sees a list of questions with radio buttons to vote
        questions = self.browser.find_elements(By.CLASS_NAME, "question")
        self.assertTrue(len(questions) > 0)

        # User selects a question and votes for it
        selected_question = questions[0]
        question_text = selected_question.find_element(By.CLASS_NAME, "question-text").text
        vote_button = selected_question.find_element(By.CLASS_NAME, "vote-button")
        vote_button.click()

        time.sleep(1)
        # User sees their voted item listed
        voted_items = self.browser.find_element(By.ID, "voted-items")
        voted_items_texts = [item.text for item in voted_items.find_elements(By.TAG_NAME, "li")]

        self.assertIn(question_text, voted_items_texts)

    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element(By.ID, "id_list_table")
    #     rows = table.find_elements(By.TAG_NAME, "tr")
    #     self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(('%s%s' % (self.live_server_url, '/polls/todo/')))

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(('%s%s' % (self.live_server_url, '/polls/todo')))
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,  "polls/todo/lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We delete all the browser's cookies
        ## as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(('%s%s' % (self.live_server_url, '/polls/todo')))
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "polls/todo/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep



class UsersAPITest(unittest.TestCase):
    fixtures = ['sample.json']  # Load sample data before running tests

    @classmethod
    def setUp(self):
        self.browser = webdriver.Firefox()
          # Change this to the appropriate WebDriver for your browser

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    def test_user_list_count(self):
        self.browser.get("http://localhost:8000/polls/users")
        user_list = self.browser.find_element(By.ID, "user-list")
        user_items = user_list.find_elements(By.TAG_NAME, "li")
        self.assertEqual(len(user_items), 5)

    def test_user_details_id(self):
        id = 2
        response = self.browser.get(f'http://localhost:8000/polls/users/{id}/')
        self.assertIn("User Details", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("User Details", header_text)







if __name__ == "__main__":
    unittest.main()