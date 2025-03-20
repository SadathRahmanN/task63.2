from django.urls import path, include
from .views import (
    HomeView,
    DestinationListView,
    DestinationDetailView,
    DashboardView,
    DestinationCreateView,
    DestinationUpdateView,
    DestinationDeleteView,
    ToggleFavoriteView,
    login_view,
    signup_view,
    logout_view,
    AdminDashboardView
)

urlpatterns = [
    # Public views
    path('', HomeView.as_view(), name='home'),
    path('destinations/', DestinationListView.as_view(), name='destination_list'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination_detail'),
    path('api/v1/', include('destinations.api.urls')),

    # Authentication
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),

    # User dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('destinations/create/', DestinationCreateView.as_view(), name='destination_create'),
    path('destinations/<int:pk>/update/', DestinationUpdateView.as_view(), name='destination_update'),
    path('destinations/<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination_delete'),
    path('destinations/<int:pk>/toggle-favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

    # Admin dashboard
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]