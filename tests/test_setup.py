import pdb
# from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestSetUp(APITestCase):

    def setUp(self):
        self.notes_url = reverse('Notes')
        self.register_url = reverse('signup')
        self.login_url = reverse('login')
        self.token_url = reverse('token_obtain_pair')
        self.label_url = reverse('label')

        self.client = APIClient()
        data = {
            "first_name": "Tanvi",
            "last_name": "Raj",
            "email": "tanvi@gmail.com",
            "address": "vit",
            "phone": "1234567",
            "username": "tanvi",
            "password": "tanvi"
        }
        response = self.client.post(self.register_url, data=data)

        self.note_data = {
            "title": "My Note",
            "description": "This is a test note",
            "isArchive": False,
            "isTrash": False,
            "color": "white"
        }

        self.label_data = {
            "name": "label-1",

        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def get_token(self):
        login_data = {'username': 'tanvi', 'password': 'tanvi'}
        response = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']
