from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from apps.fakecsv.models import Schema, Column
from apps.fakecsv.forms import SchemaForm


class SchemaListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.schema = Schema.objects.create(name='Test Schema', owner=self.user)

    def test_schema_list_authenticated_user(self):
        """
        Test that an authenticated user can access the schema list.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('fakecsv:schema_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fakecsv/schema/schema_list.html')
        self.assertContains(response, 'Test Schema')

    def test_schema_list_unauthenticated_user(self):
        """
        Test that an unauthenticated user is redirected to the login page.
        """
        url = reverse('fakecsv:schema_list')
        response = self.client.get(url)
        redirect_url = response.url
        expected_redirect_url = '/accounts/login/?next=' + url
        self.assertEqual(redirect_url, expected_redirect_url)

    def test_schema_list_context(self):
        """
        Test the context data returned by the schema list view.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('fakecsv:schema_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['schema']), [self.schema])
