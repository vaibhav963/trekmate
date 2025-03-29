from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Trek, Booking
from .forms import TrekForm,UserRegisterForm,BookingForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render
from .models import Trek

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

def view_all_treks(request):
    treks = Trek.objects.all()
    
    # Get filter values from GET request
    difficulty = request.GET.get('difficulty')
    location = request.GET.get('location')
    date = request.GET.get('date')

    # Apply filters
    if difficulty:
        treks = treks.filter(difficulty=difficulty)
    if location:
        treks = treks.filter(location__icontains=location)
    if date:
        treks = treks.filter(date=date)

    return render(request, 'trek_planner/all_treks.html', {'treks': treks})

# Add a new trek
@login_required
@user_passes_test(is_admin)
def add_trek(request):
    if request.method == 'POST':
        form = TrekForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_all_treks')
    else:
        form = TrekForm()
    return render(request, 'trek_planner/add_trek.html', {'form': form})

# Edit an existing trek
@login_required
@user_passes_test(is_admin)
def edit_trek(request, trek_id):
    trek = get_object_or_404(Trek, id=trek_id)
    if request.method == 'POST':
        form = TrekForm(request.POST, request.FILES, instance=trek)
        if form.is_valid():
            form.save()
            return redirect('view_all_treks')
    else:
        form = TrekForm(instance=trek)
    return render(request, 'trek_planner/edit_trek.html', {'form': form})

# Delete a trek (use POST for safety)
@login_required
@user_passes_test(is_admin)
def delete_trek(request, trek_id):
    Trek.objects.get(id=trek_id).delete()
    return redirect('view_all_treks')

# Book a trek
@login_required
def book_trek(request, trek_id):
    trek = get_object_or_404(Trek, id=trek_id)

    # Check if the user has already booked this trek
    if Booking.objects.filter(user=request.user, trek=trek).exists():
        messages.error(request, "You have already booked this trek.")
        return redirect('view_all_treks')

    # Check if the trek is fully booked
    if trek.booking_set.count() >= trek.max_participants:
        messages.warning(request, "This trek is fully booked!")
        return redirect('view_all_treks')

    if request.method == 'POST':
        form = BookingForm(request.POST,request.FILES)  
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.trek = trek
            booking.status = 'Pending'  # Set status to pending
            booking.save()
            messages.success(request, "Your booking has been submitted! Please wait for admin approval.")
            return redirect('user_bookings')
        else:
            messages.error(request, "Error submitting booking form.")
    else:
        form = BookingForm()

    return render(request, 'trek_planner/book_trek.html', {'form': form, 'trek': trek})


@login_required
@user_passes_test(is_admin)
def admin_bookings(request):
    # Using select_related to reduce database hits when accessing user and trek info.
    bookings = Booking.objects.all().select_related('user', 'trek')
    return render(request, 'trek_planner/admin_bookings.html', {'bookings': bookings})

# View user bookings
@login_required
def user_bookings(request):
    #messages.success(request, "Trek booked successfully!")
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'trek_planner/bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def admin_trek_detail(request, trek_id):
    trek = get_object_or_404(Trek, id=trek_id)
    bookings = trek.booking_set.all()  # or trek.bookings.all() if you set a related_name
    return render(request, 'trek_planner/admin_trek_detail.html', {'trek': trek, 'bookings': bookings})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserRegisterForm()
    return render(request, 'trek_planner/register.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
    return render(request, 'trek_planner/login.html')

# User logout
def user_logout(request):
    logout(request)
    return redirect('homepage')

# Approve or reject a booking 
@login_required
@user_passes_test(is_admin)
def approve_reject_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)

    if action == 'approve':
        if not booking.payment_screenshot:
            messages.error(request, "Cannot approve without payment proof!")
            return redirect('view_all_treks')

        booking.status = 'Approved'
        messages.success(request, f"Booking for {booking.user.username} has been approved.")

    elif action == 'reject':
        booking.status = 'Rejected'
        messages.error(request, f"Booking for {booking.user.username} has been rejected.")

    booking.save()
    return redirect('view_all_treks')

def aboutus(request):
    return render(request, 'trek_planner/aboutus.html')

@login_required
def profile(request):
    return render(request, 'trek_planner/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'trek_planner/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})