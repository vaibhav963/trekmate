from django.contrib import admin
from .models import Trek, Booking,UserProfile
# Register your models here.

class TrekAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'price', 'max_participants')
    search_fields = ('name', 'location')
    list_filter = ('date', 'difficulty')

# Define inline editing for the Booking model
class BookingInline(admin.TabularInline):  
    model = Booking  # Booking model is linked here
    extra = 1  # Displays one empty form for quick booking addition

# Customize the Trek model admin to include inline bookings
class TrekAdmin(admin.ModelAdmin):  
    inlines = [BookingInline]  # Adds booking management inside Trek admin page


admin.site.register(Trek,TrekAdmin)
admin.site.register(Booking)
#admin.site.register(UserProfile)
admin.site.site_title = 'TrekMate Admin'
admin.site.site_header = 'TrekMate Admin Panel'
admin.site.index_title = 'Welcome to TrekMate Administration'


