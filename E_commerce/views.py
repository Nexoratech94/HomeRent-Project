from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, Cart, CartItem, Order, OrderItem
from decimal import Decimal
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal
from .models import Order, Cart
from sslcommerz_lib import SSLCOMMERZ
from django.contrib.auth.decorators import login_required
from .models import CartItem
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

 
from django.db.models import Q

def medicine(request):
    search_query = request.GET.get('search')
    medicines = Medicine.objects.all()

    if search_query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=search_query) |
            Q(category__cat_Name__icontains=search_query)
        )

    return render(request, 'E_commerce/medicine.html', {'medicines': medicines})

def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    return render(request, 'E_commerce/medicine_detail.html', {'medicine': medicine})


@login_required(login_url='login')
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        return redirect('login') 
    # Add the medicine to the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
        price=medicine.price 
    )
    cart_item.quantity += 1
    cart_item.save()

    return redirect('medicine') 
 


@login_required(login_url='login')
def remove_from_cart(request, medicine_id):
    # Retrieve the cart item to remove
    cart_item = CartItem.objects.filter(cart__user=request.user, medicine_id=medicine_id).first()
    
    if cart_item:
        cart_item.delete()
        return redirect('cart')
    else:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)



@login_required(login_url='login')
def update_cart(request, medicine_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('dynamic_quantity'))
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        # Get or create the user's cart
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            return redirect('login')
        
        # Add the medicine to the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            medicine=medicine,
            price=medicine.price 
        )
        cart_item.quantity += quantity  # Increment the quantity
        cart_item.save()

        return redirect('cart')
    else:
        return redirect('home')



@login_required(login_url='login')
def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity_change = int(request.POST.get('quantity_change'))
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.quantity + quantity_change > 0:  # Ensure quantity is always positive
            cart_item.quantity += quantity_change
            cart_item.save()         
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    subtotal = cart_items.aggregate(total=Sum('subtotal'))['total'] or Decimal(0)
    delivery_charge = Decimal('100.00')
    total_price = subtotal + delivery_charge if subtotal else 0

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total_price': total_price,
        'delivery_charge': delivery_charge,
    }
    return render(request, 'E_commerce/cart.html', context)
 
 
def create_order(request, total_amount):
    if request.method == 'POST':
        user = request.user
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        address = request.POST.get('address')
        address_line2 = request.POST.get('address_line2', '')
        city_town = request.POST.get('city_town')
        state = request.POST.get('state')
        postcode_zip = request.POST.get('postcode_zip')
        phone_number = request.POST.get('phone_number')
        order_notes = request.POST.get('order_notes')
        payment_status = 'pending'

        if all([fname, lname, address, city_town, state, postcode_zip, phone_number]):
            # Create the order object
            order = Order.objects.create(
                user=user,
                fname=fname,
                lname=lname,
                address=address,
                address_line2=address_line2,
                city_town=city_town,
                state=state,
                postcode_zip=postcode_zip,
                phone_number=phone_number,
                order_notes=order_notes,
                payment_status=payment_status,
                total_amount=total_amount
            )
            return order

    return None
 

@login_required(login_url='login')
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_cart = Cart.objects.filter(user=request.user).first()
    if not user_cart or not user_cart.cartitem_set.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('Home')
    
    cart_items = user_cart.cartitem_set.all()
    cart_total = cart_items.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
    shipping_cost = Decimal('100.00')
    total_amount = cart_total + shipping_cost

    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')

        if payment_option == 'sslcommerz_payment':
            sslcz = SSLCOMMERZ({
                'store_id': 'niyam6412dc52e1e89',
                'store_pass': 'niyam6412dc52e1e89@ssl',
                'issandbox': True
            })

            data = {
                'total_amount': str(total_amount),  # Ensure the value is a string
                'currency': 'BDT',
                'tran_id': 'tran_12345',
                'success_url': 'http://127.0.0.1:8000/payment/success/',
                'fail_url': 'http://127.0.0.1:8000/payment/fail/',
                'cancel_url': 'http://127.0.0.1:8000/payment/cancel/',
                'emi_option': '0',
                'cus_name': 'test',
                'cus_email': 'test@test.com',
                'cus_phone': '01700000000',
                'cus_add1': 'customer address',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'multi_card_name': '',
                'num_of_item': 1,
                'product_name': 'Test',
                'product_category': 'Test Category',
                'product_profile': 'general',
            }

            response = sslcz.createSession(data)
            return redirect(response['GatewayPageURL'])

        elif payment_option == 'cash_on_delivery':
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            address = request.POST.get('address')
            address_line2 = request.POST.get('address_line2', '')
            city_town = request.POST.get('city_town')
            state = request.POST.get('state')
            postcode_zip = request.POST.get('postcode_zip')
            phone_number = request.POST.get('phone_number')
            order_notes = request.POST.get('order_notes')
            payment_status = 'pending'

            if all([fname, lname, address, city_town, state, postcode_zip, phone_number]):
                # Create the order object
                order = Order.objects.create(
                    user=request.user,
                    fname=fname,
                    lname=lname,
                    address=address,
                    address_line2=address_line2,
                    city_town=city_town,
                    state=state,
                    postcode_zip=postcode_zip,
                    phone_number=phone_number,
                    order_notes=order_notes,
                    payment_status=payment_status,
                    total_amount=total_amount,
                    payment_option=payment_option  # Save the selected payment method
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        medicine=cart_item.medicine,
                        quantity=cart_item.quantity,
                        price=cart_item.medicine.price,
                        subtotal=cart_item.subtotal
                    )

                # Clear cart items associated with the user
                user_cart.cartitem_set.all().delete()

                messages.success(request, 'Your order has been placed successfully.')
                return redirect(reverse('order_confirmation', kwargs={'order_id': order.id}))
            else:
                messages.error(request, 'Invalid form submission. Please check your input.')

    return render(request, 'E_commerce/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'total_amount': total_amount,
    })


@login_required(login_url='login')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'E_commerce/invoice.html', {'order': order, 'order_items': order_items})



