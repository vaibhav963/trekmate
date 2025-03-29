from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
                                
urlpatterns = [
    path('', views.view_all_treks, name='homepage'),
    path('treks/', views.view_all_treks, name='view_all_treks'),
    path('treks/add/', views.add_trek, name='add_trek'),
    path('treks/edit/<int:trek_id>/', views.edit_trek, name='edit_trek'),
    path('delete_trek/<int:trek_id>/', views.delete_trek, name='delete_trek'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('bookings/book/<int:trek_id>/', views.book_trek, name='book_trek'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard1/', views.admin_bookings, name='admin_bookings'), ####################pending
    path('dashboard/trek/<int:trek_id>/', views.admin_trek_detail, name='admin_trek_detail'),
    path('admin/bookings/<int:booking_id>/<action>/', views.approve_reject_booking, name='approve_reject_booking'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),    

]+static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
