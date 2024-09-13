from decimal import Decimal
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render,redirect
from E_commerce.models import Cart, Order
from Home_system.models import Booking, ContactForm, Location, Room, RoomCategory
from Sequrity.models import OwnerProfile, UserProfile
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_login')
def admin_panel(request):
    super_username = request.user.username
    booking=Booking.objects.all()
    total_carts = Cart.objects.count()
    total_amount_sum = Order.objects.filter(payment_status='paid').aggregate(total_amount_sum=Sum('total_amount'))['total_amount_sum']
    total_amount = round(total_amount_sum, 2) if total_amount_sum is not None else Decimal('0.00')
    total_orders = Order.objects.filter(payment_status='paid').count()
    pending_orders_count = Order.objects.filter(payment_status='pending').count()
    total_registered_renters = UserProfile.objects.count()
    total_registered_owners = OwnerProfile.objects.count()
    total_available_rooms = Room.objects.exclude(booking__booking_status='accept').distinct().count()
    total_accepted_bookings = Booking.objects.filter(booking_status='accept').count()
    
    context = {
        'total_accepted_bookings': total_accepted_bookings,
        'total_available_rooms': total_available_rooms,
        'total_registered_owners': total_registered_owners,
        'total_registered_renters': total_registered_renters,
        'total_orders': total_orders,
        'pending_orders_count': pending_orders_count,
        'total_amount': total_amount,
        'total_carts': total_carts,
        'booking':booking,
        'super_username': super_username,
        
    }
    
    return render(request, 'Adminpannel/index.html', context)


@login_required(login_url='admin_login')
def all_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'Adminpannel/all_booking.html', {'bookings': bookings})

 

@login_required(login_url='admin_login')
def Accept_all_booking(request):
    accepted_bookings = Booking.objects.filter(booking_status='accept')
    return render(request, 'Adminpannel/accept_booking.html', {'bookings': accepted_bookings})

 
@login_required(login_url='admin_login')
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id)
        new_status = request.POST.get('booking_status')
        booking.booking_status = new_status
        booking.save()
        return redirect('all_booking') 


@login_required(login_url='admin_login')
def edit_booking(request):
    return render(request,'Adminpannel/edit_booking.html')


def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('all_booking')

@login_required(login_url='admin_login')
def edit_book(request, booking_id):
    # Retrieve the booking object using the provided booking_id
    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        # Update the booking object with the data from the form
        booking.booking_id = request.POST.get('booking_id')
        booking.name = request.POST.get('name')
        booking.phone = request.POST.get('phone')
        booking.address = request.POST.get('address')
        booking.email = request.POST.get('email')
        booking.total_member = request.POST.get('total_member')
        booking.booking_status = request.POST.get('booking_status')
        booking.booking_month = request.POST.get('booking_month')

        # Check if new images are uploaded
        if request.FILES.get('renter_image'):
            booking.renter_image = request.FILES['renter_image']
        if request.FILES.get('nid_image'):
            booking.nid_image = request.FILES['nid_image']

        booking.save()

        # Redirect to a success page or another appropriate URL
        return redirect('all_booking')
    else:
        # Render the edit booking form with the existing booking data
        return render(request, 'Adminpannel/edit_booking.html', {'booking': booking})


def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'Adminpannel/room/rooms.html', {'rooms': rooms})

def delete_rooms(request, room_id):
    room = Room.objects.get(room_id=room_id)
    room.delete()
    return redirect('rooms')


from django.contrib.auth.models import User

 

def add_rooms(request):
    if request.method == 'POST':
        owner_profile_id = request.POST.get('owner_profile')
        category_id = request.POST.get('category')
        location_id = request.POST.get('location')

        # Check if the provided foreign key values exist
        if not (owner_profile_id and category_id and location_id):
            return HttpResponseBadRequest("Invalid data submitted")

        # Check if 'superuser' is selected
        if owner_profile_id == 'superuser':
            # Get the superuser instance or create it if it doesn't exist
            user_instance, created = User.objects.get_or_create(username='superuser')
            owner_profile = None  
        else:
            try:
                owner_profile = OwnerProfile.objects.get(pk=owner_profile_id)
                user_instance = owner_profile.user
            except OwnerProfile.DoesNotExist:
                return HttpResponseBadRequest("Invalid data submitted")

        try:
            category = RoomCategory.objects.get(pk=category_id)
            location = Location.objects.get(pk=location_id)
        except (RoomCategory.DoesNotExist, Location.DoesNotExist):
            return HttpResponseBadRequest("Invalid data submitted")

        # Create and save the room instance
        room = Room(
            owner=user_instance,
            category=category,
            location=location,
            description=request.POST.get('description'),
            house_number=request.POST.get('house_number'),
            road_number=request.POST.get('road_number'),
            block_number=request.POST.get('block_number'),
            street=request.POST.get('street'),
            special_identification=request.POST.get('special_identification'),
            house_type=request.POST.get('house_type'),
            rental_amount=request.POST.get('rental_amount'),
            size=request.POST.get('size'),
            bedrooms=request.POST.get('bedrooms'),
            service_charge=request.POST.get('service_charge'),
            geolocation=request.POST.get('geolocation'),  # Changed to lowercase 'g'
            location_name=request.POST.get('location_name'),
            facility1=request.POST.get('facility1'),
            facility2=request.POST.get('facility2'),
            facility3=request.POST.get('facility3'),
            facility4=request.POST.get('facility4'),
            floor_number=request.POST.get('floor_number'),
            image1=request.FILES.get('image1'),
            image2=request.FILES.get('image2'),
            image3=request.FILES.get('image3'),
            video=request.FILES.get('video')
        )
        room.save()
        return redirect('rooms')
    else:
        # Fetch categories and locations to populate dropdowns
        categories = RoomCategory.objects.all()
        locations = Location.objects.all()
        owner_profiles = OwnerProfile.objects.all()
        return render(request, 'Adminpannel/room/add_rooms.html', {'categories': categories, 'locations': locations, 'owner_profiles': owner_profiles})

 
def edit_rooms(request, room_id):
    room = Room.objects.get(room_id=room_id)
    categories = RoomCategory.objects.all()
    locations = Location.objects.all()
    if request.method == 'POST':
        # Update room data based on form submission
        room.category_id = request.POST.get('category')
        room.location_id = request.POST.get('location')
        room.house_type = request.POST.get('house_type')
        room.house_number = request.POST.get('house_number')
        room.road_number = request.POST.get('road_number')
        room.bedrooms = request.POST.get('bedrooms')
        room.size = request.POST.get('size')
        room.floor_number = request.POST.get('floor_number')
        room.block_number = request.POST.get('block_number')
        room.street = request.POST.get('street')
        room.special_identification = request.POST.get('special_identification')
        room.rental_amount = request.POST.get('rental_amount')
        room.service_charge = request.POST.get('service_charge')
        room.description = request.POST.get('description')
        room.geolocation = request.POST.get('geolocation')   
        room.location_name = request.POST.get('location_name')  
        room.facility1 = request.POST.get('facility1')
        room.facility2 = request.POST.get('facility2')
        room.facility3 = request.POST.get('facility3')
        room.facility4 = request.POST.get('facility4')
        if request.FILES.get('image1'):
            room.image1 = request.FILES['image1']
        if request.FILES.get('image2'):
            room.image2 = request.FILES['image2']
        if request.FILES.get('image3'):
            room.image3 = request.FILES['image3']
        if request.FILES.get('video'):
            room.video = request.FILES['video']
        room.save()
        return redirect('rooms')  # Redirect to room list page after editing
    else:
        return render(request, 'Adminpannel/room/edit_room.html', {'room': room, 'categories': categories, 'locations': locations})



def calendar(request):
    return render(request, 'Adminpannel/calendar.html')

def maintain(request):
    return render(request, 'Adminpannel/maintain.html')


def requestmassge(request):
    messages = ContactForm.objects.all()
    return render(request, 'Adminpannel/adminmassge/requestmassge.html',locals())