from django.urls import path
from .views import ActionList, ActionDetail

urlpatterns = [
    path('actions/', ActionList.as_view(), name='action-list'),
    path('actions/<int:pk>/', ActionDetail.as_view(), name='action-detail'),
]
