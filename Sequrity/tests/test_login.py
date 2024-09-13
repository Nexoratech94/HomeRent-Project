from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Sequrity.models import UserProfile

class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', is_active=True)
        self.user_profile = UserProfile.objects.create(user=self.user, email='testuser@example.com', email_verified=True)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to home page
        self.assertTrue(self.client.login(username='testuser', password='password123'))
