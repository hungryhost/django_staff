from django.urls import path, re_path
from django.views.decorators.http import require_POST

from .views import main, lock_incoming, IncomingDetailView, approve_request, decline_request, SalesDeleteView, \
    IncomingListView, get_lock_count

urlpatterns = [
    path('', main, name='sales-main'),
    path('inbox/', IncomingListView.as_view(), name='sales-incoming'),
    path('inbox/<int:pk>/', IncomingDetailView.as_view(), name='sales-detail'),
    path('inbox/<int:pk>/approve/', approve_request, name='sales-approve'),
    path('inbox/<int:pk>/delete/', SalesDeleteView.as_view(), name='sales-delete'),
    path('inbox/ajax/lock-count/', get_lock_count, name='sales-ajax-lock-count'),
]