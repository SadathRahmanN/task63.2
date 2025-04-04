from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Destination
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Public Views
class HomeView(ListView):
    template_name = 'destinations/home.html'
    context_object_name = 'featured_destinations'
    paginate_by = 3

    def get_queryset(self):
        return Destination.featured_destinations().order_by('-created_at')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_destinations'] = Destination.recent_destinations()[:3]
        return context

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/list.html'
    context_object_name = 'destinations'
    paginate_by = 9
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        state_filter = self.request.GET.get('state')
        sort = self.request.GET.get('sort', '-created_at')

        if search_query:
            queryset = queryset.filter(
                Q(place_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(state__icontains=search_query)
            )
        
        if state_filter:
            queryset = queryset.filter(state__iexact=state_filter)

        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_users': User.objects.filter(is_active=True).count(),
            'states': Destination.objects.values_list('state', flat=True).distinct(),
            'current_sort': self.request.GET.get('sort', '-created_at'),
            'current_state': self.request.GET.get('state')
        })
        return context

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_destinations'] = Destination.objects.filter(
            state=self.object.state
        ).exclude(pk=self.object.pk)[:4]
        
        if self.request.user.is_authenticated:
            context['is_favorite'] = self.object.favorited_by.filter(
                pk=self.request.user.pk
            ).exists()
        return context

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
            
        messages.error(request, 'Invalid username or password')
        return redirect('home')
        
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        
        # Store form errors in session for retrieval
        request.session['signup_errors'] = form.errors.get_json_data()
        request.session['signup_form_data'] = request.POST
        return redirect(f"{reverse('home')}?show_signup=true")
    
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

# User Dashboard Views
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'destinations/dashboard.html'
    context_object_name = 'created_destinations'
    paginate_by = 8

    def get_queryset(self):
        return Destination.objects.filter(created_by=self.request.user).select_related('created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'favorite_destinations': user.favorite_destinations.select_related('created_by'),
            'stats': {
                'total_created': self.get_queryset().count(),
                'total_favorites': user.favorite_destinations.count(),
                'active_users': User.objects.filter(is_active=True).count()
            }
        })
        return context

class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    fields = ['place_name', 'description', 'weather', 'state', 'district', 
              'google_map_link', 'image', 'is_featured']
    template_name = 'destinations/create.html'
    success_url = reverse_lazy('destination_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Destination created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below")
        return super().form_invalid(form)

class DestinationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Destination
    fields = ['place_name', 'description', 'weather', 'state', 'district',
              'google_map_link', 'image', 'is_featured']
    template_name = 'destinations/update.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Destination updated successfully!')
        return super().form_valid(form)

class DestinationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Destination
    template_name = 'destinations/delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Destination deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Admin Dashboard View
@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(ListView):
    model = Destination
    template_name = 'destinations/admin_dashboard.html'
    context_object_name = 'destinations'
    paginate_by = 20
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_destinations': Destination.objects.count()
        }
        return context

# Favorite Functionality
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        user = request.user

        if destination.favorited_by.filter(id=user.id).exists():
            destination.favorited_by.remove(user)
            action = 'removed from'
        else:
            destination.favorited_by.add(user)
            action = 'added to'

        messages.success(request, f"Destination {action} your favorites!")
        return redirect('destination_detail', pk=pk)