from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Sequrity.models import UserProfile

class EmailVerificationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password123', is_active=False)
        self.user_profile = UserProfile.objects.create(user=self.user, email='testuser@example.com', otp='123456')

    def test_email_verification(self):
        response = self.client.get(reverse('verify_email', args=[self.user_profile.id, '123456']))
        self.user.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user_profile.email_verified)
