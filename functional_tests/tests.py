from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest

class NewVisitorTest(LiveServerTestCase):

    #User opens firefox
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def testCanStartListForOneUser(self):
        #User loads the To-Do Lists webpage
        self.browser.get(self.live_server_url)

        #check that the title is all good
        self.assertIn('To-Do Lists',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        #User is prompted to make a new to-do list item
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        inputBox.send_keys('Buy Beer')
        inputBox.send_keys(Keys.ENTER)

        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Buy vegan hummus')
        inputBox.send_keys(Keys.ENTER)

        self.checkForRowInTable('1: Buy Beer')
        self.checkForRowInTable('2: Buy vegan hummus')


    def testMultipleUsersCanStartListsAtDifURLS(self):
        #start a new list
        self.browser.get(self.live_server_url)
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Buy Beer')
        inputBox.send_keys(Keys.ENTER)

        self.checkForRowInTable('1: Buy Beer')

        user1ListUrl = self.browser.current_url
        self.assertRegex(user1ListUrl,'/lists/.+')


        ##Use a new browser session to ensure that no info for user1's lists
        ##are coming through cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #welcome user2, make sure user1's list isn't here.
        self.browser.get(self.live_server_url)
        pageText = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy Beer',pageText)
        self.assertNotIn('vegan',pageText)

        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Buy wine')
        inputBox.send_keys(Keys.ENTER)
        self.checkForRowInTable('Buy wine')

        #user2 gets their own URL
        user2ListUrl = self.browser.current_url
        self.assertRegex(user2ListUrl,'/lists/.+')
        self.assertNotEqual(user2ListUrl,user1ListUrl)

        pageText = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy Beer',pageText)
        self.assertIn('Buy wine',pageText)


    def checkForRowInTable(self, rowText):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(rowText,[row.text for row in rows])

    #User peaces out.
    def tearDown(self):
        self.browser.quit()
