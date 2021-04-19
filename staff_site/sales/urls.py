from django.urls import path
from .views import main, lock_incoming, IncomingDetailView, approve_request, decline_request

urlpatterns = [
    path('', main, name='sales-main'),
    path('inbox/', lock_incoming, name='sales-incoming'),
    path('inbox/<int:pk>/', IncomingDetailView.as_view(), name='sales-detail'),
    path('inbox/<int:pk>/approve/', approve_request, name='sales-approve'),
    path('inbox/<int:pk>/decline/', decline_request, name='sales-decline'),
]