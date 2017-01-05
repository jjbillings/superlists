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

    def testOnlySavesItemsWhenNecessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)


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

class ListViewTest(TestCase):

    def testShouldUseListTemplate(self):
        response = self.client.get('/lists/the-only-list-ever/')
        self.assertTemplateUsed(response,'list.html')

    def testShouldDisplayAllListItems(self):
        Item.objects.create(text="item1")
        Item.objects.create(text="item2")

        response = self.client.get('/lists/the-only-list-ever/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

class NewListTest(TestCase):

    def testCanSavePOSTRequest(self):
        self.client.post('/lists/new',data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testShouldRedirectAfterPOST(self):
        response = self.client.post('/lists/new',data={'item_text': 'A new list item'})

        self.assertRedirects(response,'/lists/the-only-list-ever/')
