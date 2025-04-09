# destinations/urls.py
from django.urls import path, include
from .views import (
    HomeView,
    DestinationListView,
    DestinationDetailView,
    LoginView,
    SignupView,
    LogoutView,
    DashboardView,
    DestinationCreateView,
    DestinationUpdateView,
    DestinationDeleteView,
    ToggleFavoriteView,
    AdminDashboardView
)

urlpatterns = [
    # Public views
    path('', HomeView.as_view(), name='home'),
    path('destinations/', DestinationListView.as_view(), name='destination_list'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination_detail'),
    path('api/v1/', include('destinations.api.urls')),

    # Authentication (updated to class-based views)
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('destinations/create/', DestinationCreateView.as_view(), name='destination_create'),
    path('destinations/<int:pk>/update/', DestinationUpdateView.as_view(), name='destination_update'),
    path('destinations/<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination_delete'),
    path('destinations/<int:pk>/toggle-favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

    # Admin dashboard
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]