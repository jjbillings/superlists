from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
# Create your tests here.
class HomePageTest(TestCase):

    def testHomePageReturnsGoodHtml(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
