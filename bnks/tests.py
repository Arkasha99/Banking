from django.test import TestCase
from . models import Client, Payment, Payback


class ModelTesting(TestCase):

    def test_post_model(self):
        client = Client.objects.create(email='123asdas@mail.ru', full_name='Arkadiy Govno')
        self.assertTrue(isinstance(client, Client))
        self.assertEqual(str(client), 'Arkadiy Govno')