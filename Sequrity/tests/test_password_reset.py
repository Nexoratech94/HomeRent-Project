from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Sequrity.models import UserProfile

class PasswordResetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user, email='testuser@example.com')

    def test_password_reset(self):
        response = self.client.post(reverse('user_forgot_password'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'new_password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
