from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
# Create your tests here.
class HomePageTest(TestCase):

    def testRootURLResolvesToHomePageView(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def testHomePageReturnsGoodHtml(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do Lists</title>',html)
        self.assertTrue(html.endswith('</html>'))
