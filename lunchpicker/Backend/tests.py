# tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Restaurant, Menu, Vote

User = get_user_model()

class APITestCaseSetup(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St'
        )

        # Create a test menu
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date='2024-09-30',
            items='Pizza, Pasta, Salad'
        )

class HealthCheckTests(APITestCase):
    def test_health_check(self):
        url = reverse('health-check')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'ok'})

class RegistrationAPITests(APITestCase):
    def test_register_user(self):
        url = reverse('register')  
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_missing_fields(self):
        url = reverse('register')  
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing information for complete registration", response.data['error'])

class RestaurantAPITests(APITestCaseSetup):
    def test_create_restaurant(self):
        url = reverse('create-restaurant')  
        data = {'name': 'New Restaurant', 'address': '456 New St'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)  # Test if the restaurant is created

class MenuAPITests(APITestCaseSetup):
    def test_upload_menu(self):
        url = reverse('upload-menu')  
        data = {
            'restaurant': self.restaurant.id,
            'date': '2024-09-30',
            'items': 'Sushi, Ramen, Tempura'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)  # Test if the menu is created

    def test_get_menu(self):
        url = reverse('get-menu-by-date')  
        data = {
            'date': '2024-09-30',
            'restaurant_id': self.restaurant.id
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the menu is returned

class VoteAPITests(APITestCaseSetup):
    def test_vote_for_menu_v1(self):
        url = reverse('vote')  
        data = {
            'menu_id': self.menu.id,
            'points': 3,
            'date': '2024-09-30'
        }
        response = self.client.post(url, data, **{'MOBILE_VERSION': '1.0'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)  # Test if vote is recorded

    def test_vote_for_menu_v2(self):
        url = reverse('vote')  
        data = {
            'menu_votes': [
                {'menu_id': self.menu.id, 'points': 2}
            ],
            'date': '2024-09-30'
        }
        response = self.client.post(url, data, **{'MOBILE_VERSION': '2.0'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)  # Test if vote is recorded

    def test_vote_for_menu_invalid_api_version(self):
        url = reverse('vote')  
        data = {
            'menu_id': self.menu.id,
            'points': 3,
            'date': '2024-09-30'
        }
        response = self.client.post(url, data, **{'MOBILE_VERSION': '3.0'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid API version", response.data['error'])

class ResultsAPITests(APITestCaseSetup):
    def test_get_results(self):
        url = reverse('get-results')  
        data = {'date': '2024-09-30'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_results_no_votes(self):
        url = reverse('get-results')  
        data = {'date': '2024-09-29'}  # Date with no votes
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No votes found", response.data['error'])
