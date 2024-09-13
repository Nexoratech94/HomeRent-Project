from django.shortcuts import get_object_or_404, redirect, render
from Sequrity.models import OwnerProfile, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from decouple import config
import secrets
import logging

def userlist(request):
    userprofiles = UserProfile.objects.all()
    return render(request, 'Adminpannel/userwonerprofile/user.html', {'userprofiles': userprofiles})


def edit_userprofile(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return render(request, 'error_404.html')
    
    if request.method == 'POST':
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.phone = request.POST.get('phone')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.age = request.POST.get('age')
        user_profile.email = request.POST.get('email')
        user_profile.gender=request.POST.get('gender')
        user_profile.otp=request.POST.get('otp')
        user_profile.email_verified=request.POST.get('email_verified')
        user_profile.save()
        return redirect('userlist')  
 
    context = {
        'user_profile': user_profile
    }
    return render(request, 'Adminpannel/userwonerprofile/updateprofile.html', context)


def wonerlist(request):
    ownerprofiles = OwnerProfile.objects.all()
    return render(request, 'Adminpannel/userwonerprofile/woner.html', {'ownerprofiles': ownerprofiles})



from django.shortcuts import render, redirect, get_object_or_404
 
 

def edit_wonerprofile(request, owner_id):
    owner_profile = get_object_or_404(OwnerProfile, user_id=owner_id)

    if request.method == 'POST':
        owner_profile.first_name = request.POST.get('first_name', '')
        owner_profile.last_name = request.POST.get('last_name', '')
        owner_profile.phone = request.POST.get('phone', '')
        owner_profile.address = request.POST.get('address', '')
        owner_profile.city = request.POST.get('city', '')
        owner_profile.age = request.POST.get('age', '')
        owner_profile.email = request.POST.get('email', '')
        owner_profile.registration_status = request.POST.get('registration_status', '')

        if 'profile_image' in request.FILES:
            owner_profile.profile_image = request.FILES['profile_image']
        
        if 'nid_image' in request.FILES:
            owner_profile.nid_image = request.FILES['nid_image']
        
        owner_profile.save()
        return redirect('wonerlist')

    return render(request, 'Adminpannel/userwonerprofile/updatewonerprofile.html', {'owner_profile': owner_profile})


logger = logging.getLogger(__name__)
# Function to generate OTP
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

# Function to send verification email
def send_verification_email(request, user_profile):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('activation_email.html', {
        'user': user_profile,
        'domain': current_site.domain,
        'otp': user_profile.otp,
        'protocol': 'http',  # Adjust protocol if using HTTPS in production
    })
    to_email = user_profile.email
    try:
        send_mail(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD  # Provide authentication credentials
        )
        logger.info(f"Verification email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {to_email}: {e}")

def add_user(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST['username']
        password = request.POST['password']
        retype_password = request.POST['retype_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        city = request.POST['city']
        phone = request.POST['phone']
        email = request.POST['email']
        nid_image = request.FILES['nid_image']
        profile_image = request.FILES['profile_image']
        address = request.POST['address']

        # Validate form data
        if password != retype_password:
            messages.error(request, 'Passwords do not match. Please re-enter your password.')
            return redirect('add_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('add_user')

        # Generate OTP
        otp = generate_otp()

        # Create User object
        user = User.objects.create_user(username=username, password=password, is_active=False)

        # Create UserProfile object
        user_profile = UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            city=city,
            phone=phone,
            email=email,
            nid_image=nid_image,
            profile_image=profile_image,
            address=address,
            otp=otp
        )

        # Send verification email
        send_verification_email(request, user_profile)

        messages.success(request, 'Registration successful! Check your email for verification.')
        return redirect('add_user')
    else:
        return render(request, 'Adminpannel/userwonerprofile/add_user.html')


def add_woners(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return render(request, 'Adminpannel/userwonerprofile/add_woners.html', {'error_message': 'Username already exists. Please choose a different username.'})

            # If username is unique, proceed with registration
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                age = request.POST.get('age')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                city = request.POST.get('city')
                gender = request.POST.get('gender')
                nid_image = request.FILES.get('nid_image')
                profile_image = request.FILES.get('profile_image')
                registration_status = request.POST.get('registration_status', 'pending')

                # Check if passwords match
                if password != confirm_password:
                    return render(request, 'Adminpannel/userwonerprofile/add_woners.html', {'error_message': 'Passwords do not match'})

                # Create a new User instance
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Create a new OwnerProfile instance
                owner_profile = OwnerProfile(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    age=age,
                    phone=phone,
                    address=address,
                    city=city,
                    gender=gender,
                    nid_image=nid_image,
                    profile_image=profile_image,
                    registration_status=registration_status
                )
                owner_profile.save()

                return redirect('wonerlist')  # Redirect to the owner list page after successful creation
        except Exception as e:
            # Handle any exceptions or errors
            return render(request, 'Adminpannel/userwonerprofile/add_woners.html', {'error_message': str(e)})
    return render(request, 'Adminpannel/userwonerprofile/add_woners.html')
