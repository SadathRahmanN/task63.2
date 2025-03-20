from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Destination(models.Model):
    # Ownership and relationships
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_destinations',
        verbose_name='Created By'
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_destinations',
        blank=True,
        verbose_name='Favorited By'
    )

    # Location information
    place_name = models.CharField(
        max_length=200,
        verbose_name='Destination Name',
        help_text="Official name of the tourist destination"
    )
    state = models.CharField(
        max_length=100,
        verbose_name='State/Province',
        help_text="State or province where the destination is located"
    )
    district = models.CharField(
        max_length=100,
        verbose_name='District/County',
        help_text="District or county within the state"
    )
    
    # Descriptive fields
    description = models.TextField(
        verbose_name='Description',
        help_text="Detailed description of the location and its attractions"
    )
    weather = models.CharField(
        max_length=100,
        verbose_name='Climate',
        help_text="Typical weather conditions and climate"
    )
    
    # Media and links
    google_map_link = models.URLField(
        max_length=500,
        verbose_name='Google Maps Link',
        help_text="Full Google Maps URL for the location"
    )
    image = models.ImageField(
        upload_to='destinations/%Y/%m/%d/',
        verbose_name='Featured Image',
        help_text="Primary display image for the destination"
    )
    
    # Status flags
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Featured Destination',
        help_text="Check to highlight this as a featured destination"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation Date',
        editable=False
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modified'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tourist Destination'
        verbose_name_plural = 'Tourist Destinations'
        indexes = [
            models.Index(fields=['place_name', 'state']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.place_name}, {self.district} ({self.state})"

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'pk': self.pk})

    # Custom properties
    @property
    def favorite_count(self):
        """Returns the number of users who favorited this destination"""
        return self.favorited_by.count()

    @property
    def age_in_days(self):
        """Returns the age of the entry in days"""
        return (timezone.now() - self.created_at).days

    # Manager methods
    @classmethod
    def recent_destinations(cls, days=7):
        """Returns destinations created in the last N days"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return cls.objects.filter(created_at__gte=cutoff_date)
    
    @classmethod
    def featured_destinations(cls):
        """Returns currently featured destinations"""
        return cls.objects.filter(is_featured=True)