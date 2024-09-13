from django.shortcuts import render,redirect
from E_commerce.models import Medicine, Medicine_Catagory, Order


def orderlist(request):
    orders = Order.objects.all()
    return render(request, 'Adminpannel/ecommerceadmin/orderlist.html', {'orders': orders})

from django.db.models import Sum

 
def invoice_view(request, order_id):
    order = Order.objects.get(order_id=order_id)
    total_subtotal = order.orderitem_set.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal']
    return render(request, 'Adminpannel/ecommerceadmin/invoice_view.html', {'order': order , 'total_subtotal': total_subtotal})



def paidorder(request):
    paid_orders = Order.objects.filter(payment_status='paid')
    return render(request, 'Adminpannel/ecommerceadmin/paidorder.html', {'paid_orders': paid_orders})

 
from decimal import Decimal

def edit_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    total_subtotal = order.orderitem_set.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal']
    if request.method == 'POST':
        order.fname = request.POST.get('fname')
        order.lname = request.POST.get('lname')
        order.address = request.POST.get('address')
        order.address_line2 = request.POST.get('address_line2')
        order.city_town = request.POST.get('city_town')
        order.state = request.POST.get('state')
        order.postcode_zip = request.POST.get('postcode_zip')
        order.phone_number = request.POST.get('phone_number')
        order.order_notes = request.POST.get('order_notes')
        order.payment_status = request.POST.get('payment_status')
    
        for item in order.orderitem_set.all():
            quantity = int(request.POST.get(f'quantity_{item.id}'))
            if quantity != item.quantity:
                item.quantity = quantity
                item.subtotal = item.price * quantity
                item.save()      
        # Recalculate total amount after updating quantities
        total_subtotal = order.orderitem_set.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal']
        order.total_amount = total_subtotal+100 
        
        order.save()
        return redirect('edit_order', order_id=order_id)
    return render(request, 'Adminpannel/ecommerceadmin/edit_order.html', {'order': order, 'total_subtotal': total_subtotal})




 
def add_medicine(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        medicine_type = request.POST.get('medicine_type')
        expire_date = request.POST.get('expire_date')
        description_title = request.POST.get('description_title')
        description = request.POST.get('description')
        description_title1 = request.POST.get('description_title1')
        description1 = request.POST.get('description1')
        description_title2 = request.POST.get('description_title2')
        description2 = request.POST.get('description2')
        medicine_company = request.POST.get('medicine_company')
        medicine_company_logo = request.FILES.get('medicine_company_logo')
        medicine_image = request.FILES.get('medicine_image')

        # Get the category object based on the provided category_id
        category = Medicine_Catagory.objects.get(pk=category_id)

        # Create a new Medicine object with the retrieved data
        new_medicine = Medicine.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            medicine_type=medicine_type,
            expire_date=expire_date,
            description_title=description_title,
            description=description,
            description_title1=description_title1,
            description1=description1,
            description_title2=description_title2,
            description2=description2,
            medicine_company=medicine_company,
            medicine_company_logo=medicine_company_logo,
            medicine_image=medicine_image
        )

        # Redirect to a success page or another view
        return redirect('medicine_list')  # Change 'success_page' to the appropriate URL name

    # If it's a GET request, render the form template
    categories = Medicine_Catagory.objects.all()
    MEDICINE_TYPE_CHOICES = Medicine.MEDICINE_TYPE_CHOICES  # Retrieve medicine type choices
    return render(request, 'Adminpannel/ecommerceadmin/add_medicine.html', {'categories': categories, 'MEDICINE_TYPE_CHOICES': MEDICINE_TYPE_CHOICES})



def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'Adminpannel/ecommerceadmin/show_medicine.html', {'medicines': medicines})


from django.shortcuts import render, get_object_or_404
from datetime import datetime

def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    if request.method == 'POST':
        medicine.name = request.POST.get('name')
        medicine.price = request.POST.get('price')
        medicine.quantity = request.POST.get('quantity')
        medicine.category_id = request.POST.get('category')
        medicine.medicine_type = request.POST.get('medicine_type')
        expire_date_str = request.POST.get('expire_date')
        if expire_date_str:
            medicine.expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d').date()

        medicine.description_title = request.POST.get('description_title')
        medicine.description = request.POST.get('description')
        medicine.description_title1 = request.POST.get('description_title1')
        medicine.description1 = request.POST.get('description1')
        if request.FILES.get('medicine_company_logo'):
            medicine.medicine_company_logo = request.FILES['medicine_company_logo']
        if request.FILES.get('medicine_image'):
            medicine.medicine_image = request.FILES['medicine_image']
            
        medicine.save()
        return redirect('edit_medicine', medicine_id=medicine_id)
    
    # If it's a GET request (i.e., when the page is first loaded), render the template
    categories = Medicine_Catagory.objects.all()
    MEDICINE_TYPE_CHOICES = [
        (choice[0], choice[1]) for choice in Medicine.MEDICINE_TYPE_CHOICES
    ]
    return render(request, 'Adminpannel/ecommerceadmin/edit_medicine.html', {'medicine': medicine, 'categories': categories, 'MEDICINE_TYPE_CHOICES': MEDICINE_TYPE_CHOICES})
