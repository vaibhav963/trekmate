from django.db import models
from django.contrib.auth.models import User


class Trek(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    distance = models.FloatField()
    elevation = models.IntegerField()
    difficulty = models.CharField(
        max_length=20,
        choices=[('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')]
    )
    image = models.ImageField(upload_to='trek_images/')
    price = models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    max_participants = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    # Payment Fields
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/')

    def __str__(self):
        return f"{self.user.username} - {self.trek.name} ({self.status})" 
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
