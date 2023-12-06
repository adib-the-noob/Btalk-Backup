from . import views
from django.urls import path

urlpatterns = [
    path('create-profile/', views.ProfileView.as_view(), name='profile'),
    path('view-profile/<pk>/', views.ProfileView.as_view(), name='profile_detail'),
    path('edit-profile/', views.ProfileView.as_view(), name='profile_update'),
    path('my-profile/', views.get_my_profile, name='my_profile'),
    path('cover-photo/', views.CoverPhotoView.as_view(), name='cover_photo'),
]