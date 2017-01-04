from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

    def testUsesHomepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def testCanSavePOSTRequest(self):
        response = self.client.post('/',data={'item_text': 'A new list item'})
        self.assertIn('A new list item',response.content.decode())
        self.assertTemplateUsed(response,'home.html')

class ItemModelTest(TestCase):

    def testSavingAndRetrievingItems(self):
        firstItem = Item()
        firstItem.text = 'First List Item'
        firstItem.save()

        secondItem = Item()
        secondItem.text = 'Less exciting, second item'
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2);

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]

        self.assertEqual(firstSavedItem.text, 'First List Item')
        self.assertEqual(secondSavedItem.text, 'Less exciting, second item')
