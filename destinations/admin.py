from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = ('place_name', 'state', 'district', 'created_by', 'created_at', 'is_featured')
    list_display_links = ('place_name', 'state')
    search_fields = ('place_name', 'state', 'district', 'description', 'created_by__username')
    list_filter = ('state', 'created_at', 'is_featured')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25
    raw_id_fields = ('created_by',)

    # Detail/edit view configuration
    readonly_fields = ('created_at', 'modified_at', 'image_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('created_by', 'place_name', 'description', 'weather')
        }),
        ('Location Details', {
            'fields': ('state', 'district', 'google_map_link'),
            'description': 'Geographical and mapping details'
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Flags', {
            'fields': ('is_featured',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        })
    )

    # Image preview method
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 5px;">',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = "Preview"
    image_preview.allow_tags = True

    # Save model validation
    def save_model(self, request, obj, form, change):
        """Validate Google Maps URL format before saving"""
        valid_prefixes = (
            'https://goo.gl/maps/',
            'https://www.google.com/maps/',
            'https://maps.app.goo.gl/'
        )
        
        if not obj.google_map_link.startswith(valid_prefixes):
            raise ValidationError(
                "Invalid Google Maps URL. Please use one of these formats:\n"
                "- https://goo.gl/maps/...\n"
                "- https://www.google.com/maps/...\n"
                "- https://maps.app.goo.gl/..."
            )
        super().save_model(request, obj, form, change)

    # Admin actions
    actions = ['toggle_featured_status']

    @admin.action(description="Toggle Featured Status")
    def toggle_featured_status(self, request, queryset):
        """Bulk toggle featured status for selected destinations"""
        for destination in queryset:
            destination.is_featured = not destination.is_featured
            destination.save()
        self.message_user(
            request,
            f"Successfully toggled featured status for {queryset.count()} destinations"
        )