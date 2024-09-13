
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from E_commerce.models import Order
from Sequrity.models import OwnerProfile, UserProfile
from .models import Booking
from django.http import Http404
from .models import Room, Location, RoomCategory
from .models import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def Home(request):
    locations = Location.objects.all()
    room_categories = RoomCategory.objects.all()
    if request.method == 'GET':
        location = request.GET.get('location')
        category_name = request.GET.get('prototype')
        price_range = request.GET.get('price')
        
        if location and category_name and price_range:
            # Redirect to the search results page with the selected criteria
            return redirect('search_results', location=location, prototype=category_name, price=price_range)
    
    return render(request, 'Home.html', {'locations': locations, 'room_categories': room_categories})

  
from django.shortcuts import render
from .models import Location, RoomCategory, Room

def search(request):
    # Fetch all locations and room categories
    locations = Location.objects.all()
    room_categories = RoomCategory.objects.all()

    # Initialize an empty list for filtered rooms
    filtered_rooms = []

    if request.method == 'GET':
        # Retrieve search parameters from the GET request
        location = request.GET.get('location', None)
        category_name = request.GET.get('prototype', None)
        price_range = request.GET.get('price', None)
        
        # Handle price range filtering
        if price_range:
            try:
                # Clean and parse the price range
                price_range = price_range.replace('%20TAKA', '')
                min_price, max_price = map(int, price_range.split('-'))

                # Filter rooms based on location, category_name, and price_range
                if location and category_name:
                    filtered_rooms = Room.objects.filter(
                        location__area_location=location,
                        category__category_name=category_name,
                        rental_amount__range=(min_price, max_price)
                    )
                elif location:
                    filtered_rooms = Room.objects.filter(
                        location__area_location=location,
                        rental_amount__range=(min_price, max_price)
                    )
                elif category_name:
                    filtered_rooms = Room.objects.filter(
                        category__category_name=category_name,
                        rental_amount__range=(min_price, max_price)
                    )
                else:
                    filtered_rooms = Room.objects.filter(
                        rental_amount__range=(min_price, max_price)
                    )

            except ValueError:
                # Handle invalid price range input
                filtered_rooms = Room.objects.none()
        
        # If no price range provided, filter based on location and category_name only
        else:
            if location and category_name:
                filtered_rooms = Room.objects.filter(
                    location__area_location=location,
                    category__category_name=category_name,
                )
            elif location:
                filtered_rooms = Room.objects.filter(
                    location__area_location=location,
                )
            elif category_name:
                filtered_rooms = Room.objects.filter(
                    category__category_name=category_name,
                )

    context = {
        'locations': locations,
        'room_categories': room_categories,
        'filtered_rooms': filtered_rooms,
    }
    
    return render(request, 'search_results.html', context)



from django.db.models import Q
def room_list(request):
    rooms = Room.objects.all()
    booked_rooms_ids = Booking.objects.filter(booking_status='accept').values_list('room_id', flat=True)
    search_query = request.GET.get('search')

    if search_query:
        try:
            search_query_int = int(search_query)
            rooms = rooms.filter(
                Q(category__category_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(house_number__icontains=search_query) |
                Q(road_number__icontains=search_query) |
                Q(block_number__icontains=search_query) |
                Q(street__icontains=search_query) |
                Q(special_identification__icontains=search_query) |
                Q(house_type__icontains=search_query) |
                Q(rental_amount=search_query_int) |
                Q(size=search_query_int) |
                Q(bedrooms=search_query_int) |
                Q(location__area_location__icontains=search_query.lower())
            )
        except ValueError:
            rooms = rooms.filter(
                Q(category__category_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(house_number__icontains=search_query) |
                Q(road_number__icontains=search_query) |
                Q(block_number__icontains=search_query) |
                Q(street__icontains=search_query) |
                Q(special_identification__icontains=search_query) |
                Q(house_type__icontains=search_query) |
                Q(location__area_location__icontains=search_query.lower())
            )

    return render(request, 'room.html', {'rooms': rooms, 'booked_rooms_ids': booked_rooms_ids})


from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
 

@login_required
def add_room(request):
    locations = Location.objects.all()
    categories = RoomCategory.objects.all()
    
    if request.method == 'POST':
        category_name = request.POST.get('category')
        location_name = request.POST.get('location')
        description = request.POST.get('description')
        house_number = request.POST.get('house_number')
        road_number = request.POST.get('road_number')
        block_number = request.POST.get('block_number')
        street = request.POST.get('street')
        special_identification = request.POST.get('special_identification')
        house_type = request.POST.get('house_type')
        rental_amount = request.POST.get('rental_amount')
        size = request.POST.get('size')
        bedrooms = request.POST.get('bedrooms')
        service_charge = request.POST.get('service_charge')
        facility1 = request.POST.get('facility1')
        facility2 = request.POST.get('facility2')
        facility3 = request.POST.get('facility3')
        facility4 = request.POST.get('facility4')
        floor_number = request.POST.get('floor_number')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        video = request.FILES.get('video')
        geolocation = request.POST.get('geolocation')
        location_name_input = request.POST.get('location_name')  # Changed the variable name to avoid conflict
        
        try:
            # Get the category instance
            category = RoomCategory.objects.get(category_name=category_name)
        except RoomCategory.DoesNotExist:
            return HttpResponseNotFound("Category not found")
        
        try:
            # Get the location instance
            location = Location.objects.get(area_location=location_name)
        except Location.DoesNotExist:
            # If location does not exist, create a new one
            location = Location.objects.create(area_location=location_name)
        
        # Set the owner of the room to the current user
        owner = request.user
        
        room = Room(
            owner=owner,
            category=category,
            location=location,
            description=description,
            house_number=house_number,
            road_number=road_number,
            block_number=block_number,
            street=street,
            special_identification=special_identification,
            house_type=house_type,
            rental_amount=rental_amount,
            size=size,
            bedrooms=bedrooms,
            service_charge=service_charge,
            facility1=facility1,
            facility2=facility2,
            facility3=facility3,
            facility4=facility4,
            floor_number=floor_number,
            image1=image1,
            image2=image2,
            image3=image3,
            video=video,
            geolocation=geolocation,
            location_name=location_name_input
        )
        room.save()
        
        # Redirect to a success page or render a template indicating successful room addition
        return redirect('room')
    else:
        return render(request, 'addhouse.html', {'locations': locations, 'categories': categories})
 
@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    context = {'profile': profile}
    return render(request, 'profile.html', context)


def about(request):
    return render(request, 'ourteam.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact_form = ContactForm(name=name, phone_number=phone_number, email=email, message=message)
        contact_form.save()

        return redirect('contact')
    else:
        return render(request, 'contact.html')



@login_required
def view_owner_profile(request):
    # Retrieve the owner's profile based on the logged-in user
    profile = OwnerProfile.objects.get(user=request.user)
    rooms = Room.objects.filter(owner=request.user)
    
    # Check the registration status
    if profile.registration_status == 'accept':
        return render(request, 'wonerprofile.html', {'profile': profile, 'rooms': rooms})
    else:
        # If registration status is not 'accept', show a message or redirect to a different page
        return render(request, 'wonerprofile.html', {'profile': profile, 'rooms': rooms})


def house_details(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    description_lines = room.description.split('\n')
    
    # Ensure you import the Booking model and access MONTH_CHOICES
    MONTH_CHOICES = Booking.MONTH_CHOICES
    
    # Check if the user is an owner
    if hasattr(request.user, 'ownerprofile'):
        # Notify the owner that they cannot book the house
        messages.error(request, "You are the owner and cannot book this house.")
        return render(request, 'house_details.html', {'room': room, 'description_lines': description_lines, 'MONTH_CHOICES': MONTH_CHOICES})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        renter_image = request.FILES.get('renter_image')
        nid_image = request.FILES.get('nid_image')
        total_member = request.POST.get('total_member')
        booking_month = request.POST.get('booking_month')  # Get booking month
        
        # Get the room object
        room = get_object_or_404(Room, pk=room_id)
        user_profile = request.user.userprofile
        
        # Create the booking object with user profile
        booking = Booking.objects.create(name=name, phone=phone, address=address, email=email, renter_image=renter_image,
                                         nid_image=nid_image, total_member=total_member, room=room, user_profile=user_profile,
                                         booking_month=booking_month)  # Include booking month
        
        return redirect('room') 
    
    return render(request, 'house_details.html', {'room': room, 'description_lines': description_lines, 'MONTH_CHOICES': MONTH_CHOICES})



def Upcoming(request):
    return render(request, 'Upcoming.html')


 

@login_required
def userorderdashborde(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    
    # Determine if the user has an OwnerProfile or UserProfile
    is_owner = OwnerProfile.objects.filter(user=user).exists()
    has_profile = UserProfile.objects.filter(user=user).exists()

    return render(request, 'userorderdashbord.html', {
        'orders': orders,
        'is_owner': is_owner,
        'has_profile': has_profile,
    })


def usertotalboking(request):
    user = request.user
    bookings = Booking.objects.filter(user_profile__user=user)
    return render(request, 'usertotalboking.html', {'bookings': bookings})



from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TransportRequest

@login_required(login_url='login')
def transport(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        pickup = request.POST.get('pickup')
        dropoff = request.POST.get('dropoff')
        date = request.POST.get('date')
        time = request.POST.get('time')

        transport_request = TransportRequest(
            name=name,
            contact=contact,
            email=email,
            pickup=pickup,
            dropoff=dropoff,
            date=date,
            time=time
        )
        transport_request.save()
        return redirect('Hoom')  

    return render(request, 'transport.html')
