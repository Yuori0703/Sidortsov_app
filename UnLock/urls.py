from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('open_car/', views.OpenCar.as_view(), name='car'),
    path('open_door/', views.OpenDoor.as_view(), name='door'),
    path('open_garage/', views.OpenGarage.as_view(), name='garage'),
    path('open_safe/', views.OpenSafe.as_view(), name='safe'),
    path('replace/', views.Replace.as_view(), name='replace'),
    path('installation/', views.Installation.as_view(), name='installation'),
    path('repair/', views.Repair.as_view(), name='repair'),
    path('price_all/', views.PriceAll.as_view(), name='price_all'),
    path('register/', views.register, name='register'),
    path('create_review/', views.CreateReview.as_view(), name='create_review'),
    path('lock/', views.Lock.as_view(), name='lock'),
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('service_request/', views.service_request, name='service_request'),
    path('contact/', views.contact, name='contact'),
    path('about_us/', views.AboutUsView.as_view(), name='about_us'),


]