from django.urls import path
from . import views

urlpatterns = [
    path('get-all-notifications/', views.get_all_notifications, name='get_all_notifications'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
]