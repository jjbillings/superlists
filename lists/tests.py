from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):

    def testUsesHomepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def testOnlySavesItemsWhenNecessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)


class ListAndItemModelTest(TestCase):

    def testSavingAndRetrievingItems(self):

        list_ = List()
        list_.save()

        firstItem = Item()
        firstItem.text = 'First List Item'
        firstItem.list = list_
        firstItem.save()

        secondItem = Item()
        secondItem.text = 'Less exciting, second item'
        secondItem.list = list_
        secondItem.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2);

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]

        self.assertEqual(firstSavedItem.text, 'First List Item')
        self.assertEqual(firstSavedItem.list,list_)
        self.assertEqual(secondSavedItem.text, 'Less exciting, second item')
        self.assertEqual(secondSavedItem.list,list_)

class ListViewTest(TestCase):

    def testShouldUseListTemplate(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/'%(list_.id,))
        self.assertTemplateUsed(response,'list.html')

    def testShouldDisplayAllListItems(self):
        list_ = List.objects.create()
        Item.objects.create(text="item1",list=list_)
        Item.objects.create(text="item2",list=list_)

        otherList = List.objects.create()
        Item.objects.create(text="other item1",list=otherList)
        Item.objects.create(text="other item2",list=otherList)

        response = self.client.get('/lists/%d/'%(list_.id))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other item1')
        self.assertNotContains(response, 'other item2')

class NewListTest(TestCase):

    def testCanSavePOSTRequest(self):
        self.client.post('/lists/new',data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testShouldRedirectAfterPOST(self):
        response = self.client.post('/lists/new',data={'item_text': 'A new list item'})
        newList = List.objects.first()
        self.assertRedirects(response,'/lists/%d/'%(newList.id,))
