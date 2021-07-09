from django.urls import path

from bnks import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('profile', views.profile, name='profile'),
    path('registration/', views.RegisterView.as_view(), name='registration_view'),
]
