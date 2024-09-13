from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Staff

def addStaff(request):
    if request.method == 'POST':
        # Retrieve data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        nid_number = request.POST.get('nid_number')
        father_nid = request.POST.get('father_nid')
        mother_nid = request.POST.get('mother_nid')
        joining_date = request.POST.get('joining_date')
        leaving_time= request.POST.get('leaving_time')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        on_duty= request.POST.get('on_duty')
        image = request.FILES.get('image')
        
        # Check if all required fields are provided
        if not (first_name and last_name and email and nid_number and joining_date and phone_number and role):
            return HttpResponseBadRequest("Missing required fields")
        
        # Create a new Staff instance
        staff = Staff(
            first_name=first_name,
            last_name=last_name,
            email=email,
            nid_number=nid_number,
            father_nid=father_nid,
            mother_nid=mother_nid,
            joining_date=joining_date,
            leaving_time=leaving_time,
            phone_number=phone_number,
            role=role,
            on_duty=on_duty,
            image=image  # Assign the image to the Staff instance
        )
        # Save the new Staff instance
        staff.save()
        return redirect('all_staff')
    return render(request, 'Adminpannel/staff/addStaff.html')

# views.py

def all_staff(request):
    staff_members = Staff.objects.all()

    # Handle form submission
    if request.method == 'GET':
        staff_id = request.GET.get('staff_id')
        role = request.GET.get('role')

        # Apply filters based on search parameters
        if staff_id:
            staff_members = staff_members.filter(staff_id=staff_id)
        
        if role:
            staff_members = staff_members.filter(role=role)

    return render(request, 'Adminpannel/staff/all_staff.html', {'staff_members': staff_members})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest

def edit_staff(request, staff_id):
    # Retrieve the staff object from the database
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        # Retrieve data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        nid_number = request.POST.get('nid_number')
        father_nid = request.POST.get('father_nid')
        mother_nid = request.POST.get('mother_nid')
        joining_date = request.POST.get('joining_date')
        leaving_time= request.POST.get('leaving_time')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        on_duty= request.POST.get('on_duty')
        image = request.FILES.get('image')
        
        # Check if all required fields are provided
        if not (first_name and last_name and email and nid_number and joining_date and phone_number and role):
            return HttpResponseBadRequest("Missing required fields")
        
        # Update the staff object with the new data
        staff.first_name = first_name
        staff.last_name = last_name
        staff.email = email
        staff.nid_number = nid_number
        staff.father_nid = father_nid
        staff.mother_nid = mother_nid
        staff.joining_date = joining_date
        staff.leaving_time = leaving_time
        staff.phone_number = phone_number
        staff.role = role
        staff.on_duty = on_duty
        if image:
            staff.image = image
        
        # Save the updated staff object
        staff.save()
        
        # Redirect to the staff detail page or any other appropriate page
        return redirect('all_staff')

    
    # Render the edit staff template with the staff object
    return render(request, 'Adminpannel/staff/edit_staff.html', {'staff': staff})