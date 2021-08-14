from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]
