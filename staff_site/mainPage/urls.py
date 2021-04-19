from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='lr-main'),
    path('dash/', views.dashboard, name='lr-dashboard-main')
]