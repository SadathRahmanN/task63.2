from django.urls import path
from . import views

urlpatterns = [
    path('destinations/', views.DestinationListCreateAPIView.as_view(), name='api-destination-list'),
    path('destinations/<int:pk>/', views.DestinationRetrieveUpdateDestroyAPIView.as_view(), name='api-destination-detail'),
    path('destinations/<int:pk>/toggle-favorite/', views.ToggleFavoriteAPIView.as_view(), name='api-toggle-favorite'),
]