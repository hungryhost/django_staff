from django.urls import path
from .views import main, lock_incoming, IncomingDetailView, approve_request, decline_request

urlpatterns = [
    path('', main, name='manufacturing-main'),
    path('inbox/', lock_incoming, name='manufacturing-incoming'),
    path('inbox/<int:pk>/', IncomingDetailView.as_view(), name='manufacturing-detail'),
    path('inbox/<int:pk>/approve/', approve_request, name='manufacturing-approve'),
    path('inbox/<int:pk>/decline/', decline_request, name='manufacturing-decline'),
]