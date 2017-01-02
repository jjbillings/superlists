from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
# Create your tests here.
class HomePageTest(TestCase):

    def testRootURLResolvesToHomePageView(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
