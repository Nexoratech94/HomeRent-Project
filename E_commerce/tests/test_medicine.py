from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Medicine, Cart, CartItem, Medicine_Catagory  # Adjust import as per your actual structure

class CartTestCase(TestCase):
    
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

    def test_add_to_cart(self):
        # Add medicine1 to the cart
        response = self.client.post(reverse('add_to_cart', kwargs={'medicine_id': self.medicine1.pk}))
        
        # Check if the redirect was successful
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirect
        
        # Check if the medicine1 is in the cart
        self.assertTrue(self.cart.items.filter(medicine=self.medicine1).exists())
        
        # Check if quantity is correctly updated
        cart_item = CartItem.objects.get(cart=self.cart, medicine=self.medicine1)
        self.assertEqual(cart_item.quantity, 1)  # Assuming the default quantity is set to 1

    def test_remove_from_cart(self):
        # Add medicine1 and medicine2 to the cart
        self.cart.items.add(self.medicine1, through_defaults={'price': self.medicine1.price})
        self.cart.items.add(self.medicine2, through_defaults={'price': self.medicine2.price})
        
        # Check if both items are in the cart
        self.assertEqual(self.cart.items.count(), 2)

        # Remove medicine1 from the cart
        response = self.client.post(reverse('remove_from_cart', kwargs={'medicine_id': self.medicine1.pk}))
        
        # Check if the redirect was successful
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirect
        
        # Check if medicine1 is removed from the cart
        self.assertFalse(self.cart.items.filter(medicine=self.medicine1).exists())
        
        # Check if medicine2 still exists in the cart
        self.assertTrue(self.cart.items.filter(medicine=self.medicine2).exists())

    # Add more test cases as needed

