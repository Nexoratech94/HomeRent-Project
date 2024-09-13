from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Sequrity.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

class RegistrationTestCase(TestCase):

    def test_user_registration(self):
        # Simulate file uploads using SimpleUploadedFile
        nid_image = SimpleUploadedFile('nid_image.png', b'fake content', content_type='image/png')
        profile_image = SimpleUploadedFile('profile_image.png', b'fake content', content_type='image/png')

        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'password123',
            'retype_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'age': 25,
            'gender': 'Male',
            'city': 'Test City',
            'phone': '1234567890',
            'email': 'testuser@example.com',
            'nid_image': nid_image,
            'profile_image': profile_image,
            'address': '123 Test Street',
        })

        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(email='testuser@example.com').exists())
