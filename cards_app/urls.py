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
    path('binder/<int:card_id>/', views.card_detail, name='card-detail'),
    path('binder/<int:pk>/remove-card', views.CardDelete.as_view(), name='card-delete'),
    path('binder/<int:pk>/update-card', views.CardUpdate.as_view(), name='card-update'),
    path('binder/<int:card_id>/favorite', views.add_favorite, name='add-favorite'),
    path('binder/<int:card_id>/remove-favorite', views.remove_favorite, name='remove-favorite'),
]