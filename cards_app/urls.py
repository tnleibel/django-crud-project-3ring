from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('binder/', views.card_index, name='card-index'),
]