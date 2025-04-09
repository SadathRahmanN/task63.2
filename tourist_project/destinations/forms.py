# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Destination

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        }),
        help_text="We'll never share your email with anyone else."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update field attributes for better styling
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class DestinationForm(forms.ModelForm):

    WEATHER_CHOICES = [
        ('', 'Select Weather Type'),  # Empty placeholder
        ('Sunny', '☀️ Sunny'),
        ('Cloudy', '☁️ Cloudy'),
        ('Rainy', '🌧️ Rainy'),
        ('Snowy', '❄️ Snowy'),
        ('Windy', '🌪️ Windy'),
        ('Stormy', '⛈️ Stormy'),
        ('Foggy', '🌫️ Foggy'),
        ('Mild', '🌤️ Mild'),
    ]
    
    weather = forms.ChoiceField(
        choices=WEATHER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Weather conditions'
        }),
        required=True
    )
    
    class Meta:
        model = Destination
        fields = [
            'place_name', 
            'description', 
            'weather',
            'state', 
            'district',
            'google_map_link',
            'image',
            'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the destination'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://goo.gl/maps/...'}),
            'weather': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'is_featured': "Check this to highlight as a premium destination",
            'google_map_link': "Paste Google Maps share link here"
        }

    def clean_google_map_link(self):
        link = self.cleaned_data.get('google_map_link')
        if link and not ('google.com/maps' in link or 'maps.google.com' in link):
            raise ValidationError("Please provide a valid Google Maps link.")
        return link

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Image file too large (max 5MB).")
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Only PNG, JPG, or JPEG images are allowed.")
        return image