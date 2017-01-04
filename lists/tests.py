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

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testShouldRedirectAfterPOST(self):
        response = self.client.post('/',data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')

    def testOnlySavesItemsWhenNecessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)

    def testShouldDisplayAllListItems(self):
        Item.objects.create(text="item1")
        Item.objects.create(text="item2")

        response = self.client.get('/')

        self.assertIn('item1',response.content.decode())
        self.assertIn('item2',response.content.decode())

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
