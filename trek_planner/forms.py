from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Trek, Booking, UserProfile
from django.contrib.auth.models import User

class TrekForm(forms.ModelForm):
    class Meta:
        model = Trek
        fields = [
            'name', 'description', 'distance', 'elevation', 'difficulty', 
            'image', 'price', 'date', 'time', 'location', 'max_participants'
        ]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['payment_screenshot']
        widgets = {
            'payment_screenshot': forms.FileInput(attrs={'class': 'w-full border px-4 py-2 rounded-md'}),
        }



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_picture']