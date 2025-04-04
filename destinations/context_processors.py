# destinations/context_processors.py
from .models import Destination
from django.contrib.auth.models import User

def site_stats(request):
    return {
        'total_destinations': Destination.objects.count(),
        'total_users': User.objects.count(),
        'featured_count': Destination.objects.filter(is_featured=True).count()
    }