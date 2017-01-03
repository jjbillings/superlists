from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    #User opens firefox
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def testCanIStartAListAndRetrieveItLater(self):
        #User loads the To-Do Lists webpage
        self.browser.get("http://localhost:8000")

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == "1: Buy Beer" for row in rows),
            "New to-do item did not appear in the table :("
        )

        self.fail("Finish Test?")

    #User peaces out.
    def tearDown(self):
        self.browser.quit()
if __name__ == '__main__':
    unittest.main(warnings='ignore')
