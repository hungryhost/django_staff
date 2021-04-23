from django.urls import path
from .views import main, lock_incoming, IncomingDetailView, approve_request, decline_request, lock_create, LockListView, \
    LockDetailView, LockUpdateView, LockDeleteView, KeyUpdateView, refresh_user_docs, key_create

urlpatterns = [
    path('', main, name='manufacturing-main'),
    path('inbox/', lock_incoming, name='manufacturing-incoming'),
    path('inbox/my/', lock_incoming, name='manufacturing-incoming-my'),
    path('locks/new/', lock_create, name='manufacturing-create-lock'),
    path('locks/', LockListView.as_view(), name='manufacturing-lock-list'),
    path('locks/<int:pk>/', LockDetailView.as_view(), name='manufacturing-lock-detail'),
    path('locks/<int:pk>/update/', LockUpdateView.as_view(), name='manufacturing-lock-update'),
    path('locks/<int:pk>/update-master-key/', KeyUpdateView.as_view(),
         name='manufacturing-lock-update-master-key'),
    path('locks/<int:pk>/create-master-key/', key_create,
         name='manufacturing-lock-create-master-key'),

    path('locks/<int:pk>/update-docs/', refresh_user_docs,
         name='manufacturing-lock-update-docs'),
    path('locks/<int:pk>/delete/', LockDeleteView.as_view(), name='manufacturing-lock-delete'),
    path('inbox/<int:pk>/', IncomingDetailView.as_view(), name='manufacturing-detail'),
    path('inbox/<int:pk>/approve/', approve_request, name='manufacturing-approve'),
    path('inbox/<int:pk>/decline/', decline_request, name='manufacturing-decline'),
]