from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from E_commerce.models import Cart, Medicine, CartItem, Medicine_Catagory  # Adjust imports as per your actual structure

class CartModelTestCase(TestCase):
    
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a medicine category
        self.category = Medicine_Catagory.objects.create(cat_Name='Category Name')

        # Create some medicine items with the assigned category
        self.medicine1 = Medicine.objects.create(name='Medicine 1', price='10.00', quantity=100, category=self.category)
        self.medicine2 = Medicine.objects.create(name='Medicine 2', price='20.00', quantity=50, category=self.category)

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        # Check if a cart is created successfully for a user
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.items.count(), 0)  # Initially, no items in the cart
        self.assertTrue(self.cart.created_at)  # Ensure created_at is set

    def test_cart_str_method(self):
        # Test the string representation of the Cart model
        expected_str = f"Cart {self.cart.id} - User: {self.user.username}"
        self.assertEqual(str(self.cart), expected_str)

class CartViewTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Log in the user
        self.client.login(username='testuser', password='password123')

        # Create a medicine category
        self.category = Medicine_Catagory.objects.create(cat_Name='Category Name')

        # Create some medicine items with the assigned category
        self.medicine1 = Medicine.objects.create(name='Medicine 1', price='10.00', quantity=100, category=self.category)
        self.medicine2 = Medicine.objects.create(name='Medicine 2', price='20.00', quantity=50, category=self.category)

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

        # Add items to the cart (if needed for testing specific scenarios)

    def test_cart_view(self):
        # Test the cart view function
        response = self.client.get(reverse('cart'))

        # Check that the response status code is 200 for an authenticated user
        self.assertEqual(response.status_code, 200)

        # Check context variables
        self.assertIn('cart_items', response.context)
        self.assertIn('subtotal', response.context)
        self.assertIn('total_price', response.context)
        self.assertIn('delivery_charge', response.context)

        # Add more specific assertions based on your view's behavior and expected output

    # Add more tests as needed for edge cases and specific scenarios

    def tearDown(self):
        # Clean up after each test if needed
        pass
