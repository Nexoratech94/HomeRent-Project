from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile
from django.conf import settings
from django.contrib.auth.hashers import make_password
from decouple import config
import secrets
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Configure logging
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

 
def verify_email(request, user_id, otp):
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        user_profile.user.is_active = True
        user_profile.user.save()
        login(request, user_profile.user)
        user_profile.email_verified = True
        user_profile.save()
        messages.success(request, 'Your email has been verified. You are now logged in.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification link. Please try again.')
        return redirect('login')
    return redirect('Home')

def register(request):
    if request.method == 'POST':
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

        if password != retype_password:
            messages.error(request, 'Passwords do not match. Please re-enter your password.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('register')

        # Generate OTP
        otp = generate_otp()

        # Create User object
        user = User(
            username=username,
            password=make_password(password), 
            is_active=False
        )
        user.save()

        # Create UserProfile object
        user_profile = UserProfile(
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
        user_profile.save()

        # Send verification email
        send_verification_email(request, user_profile)

        messages.success(request, 'Registration successful! Check your email for verification.')
        return redirect('login')
    else:
        return render(request, 'registration.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.email_verified:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('Home')  # Change 'home' to your home page URL name
                else:
                    messages.error(request, 'Please verify your email before logging in.')
            except ObjectDoesNotExist:
                messages.error(request, 'Profile does not exist for this user. Please register first.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('Home') 


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import OwnerProfile

 
def woner_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'wonerregistration.html', {'error_message': 'Username already exists. Please choose a different username.'})

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
            return render(request, 'wonerregistration.html', {'error_message': 'Passwords do not match'})

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

        return redirect('woner_login')  # Redirect to a success page

    return render(request, 'wonerregistration.html')


 

def woner_login(request):
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        
        if user:
            if hasattr(user, 'ownerprofile') and user.ownerprofile.registration_status == 'accept':
                # If the user has an owner profile and their registration status is 'accept', proceed with login
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('Home')
            else:
                # If the user does not have an owner profile or their registration status is not 'accept', show notification
                return render(request, 'wonerlogin.html', {'error_message': 'You are not an owner profile. Please contact support.'})
        else:
            return render(request, 'wonerlogin.html', {'error_message': 'Invalid username or password.'})

    return render(request, 'wonerlogin.html')

from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
 
 

def ownwerforget_pass(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            owner_profile = OwnerProfile.objects.get(user=user)
            if owner_profile.email == email:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successful')
                return redirect('woner_login')
            else:
                messages.error(request, 'Email does not match.')
                return redirect('forgot')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('forgot')
        except OwnerProfile.DoesNotExist:
            messages.error(request, 'Owner profile does not exist.')
            return redirect('forgot')

    return render(request, 'ownwerforget_pass.html')


from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile

def user_forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            if profile.email == email:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successful')
                return redirect('login')  # Redirect to login page
            else:
                messages.error(request, 'Email does not match.')
                return redirect('user_forgot_password')  # Redirect back to forgot password page
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('user_forgot_password')  # Redirect back to forgot password page
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile does not exist.')
            return redirect('user_forgot_password')  # Redirect back to forgot password page

    return render(request, 'forgot_password.html')
