from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_pannel')  # Redirect to the admin panel page
        else:
            # Increment login attempts counter
            login_attempts = request.session.get('login_attempts', 0) + 1
            request.session['login_attempts'] = login_attempts

            if login_attempts >= 5:
                messages.error(request, "You have exceeded the maximum login attempts. Your account is blocked.")
                return redirect('admin_login')  # Redirect to the blocked page
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('admin_login')  # Redirect back to the login page

    return render(request, 'Adminpannel/sequrity/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

 
 
