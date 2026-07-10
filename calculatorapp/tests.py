from django.test import TestCase
from django.urls import reverse

class CalculatorAppTests(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_submitquery_page_valid(self):
        response = self.client.get(reverse('submitquery'), {'query': '2+4'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['result'], '6')
        self.assertFalse(response.context['error'])
        # Verify the result appears in the html
        self.assertContains(response, '<strong>2+4</strong> = <strong>6</strong>')

    def test_submitquery_page_invalid(self):
        response = self.client.get(reverse('submitquery'), {'query': 'import os'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['result'], 'Error: Invalid characters. Use numbers and +, -, *, /, //, (), .')
        self.assertTrue(response.context['error'])
        self.assertContains(response, 'Error: Invalid characters. Use numbers and +, -, *, /, //, (), .')

    def test_submitquery_implicit_multiplication(self):
        response = self.client.get(reverse('submitquery'), {'query': '6*2(3/5)*(45//5)'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['result'], '64.8')
        self.assertFalse(response.context['error'])
        self.assertContains(response, '<strong>6*2(3/5)*(45//5)</strong> = <strong>64.8</strong>')
