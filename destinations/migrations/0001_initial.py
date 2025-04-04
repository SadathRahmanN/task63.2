# Generated by Django 5.0.11 on 2025-02-13 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(help_text='Official name of the tourist destination', max_length=200, verbose_name='Destination Name')),
                ('state', models.CharField(help_text='State or province where the destination is located', max_length=100, verbose_name='State/Province')),
                ('district', models.CharField(help_text='District or county within the state', max_length=100, verbose_name='District/County')),
                ('description', models.TextField(help_text='Detailed description of the location and its attractions', verbose_name='Description')),
                ('weather', models.CharField(help_text='Typical weather conditions and climate', max_length=100, verbose_name='Climate')),
                ('google_map_link', models.URLField(help_text='Full Google Maps URL for the location', max_length=500, verbose_name='Google Maps Link')),
                ('image', models.ImageField(help_text='Primary display image for the destination', upload_to='destinations/%Y/%m/%d/', verbose_name='Featured Image')),
                ('is_featured', models.BooleanField(default=False, help_text='Check to highlight this as a featured destination', verbose_name='Featured Destination')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_destinations', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('favorited_by', models.ManyToManyField(blank=True, related_name='favorite_destinations', to=settings.AUTH_USER_MODEL, verbose_name='Favorited By')),
            ],
            options={
                'verbose_name': 'Tourist Destination',
                'verbose_name_plural': 'Tourist Destinations',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['place_name', 'state'], name='destination_place_n_3e35c9_idx'), models.Index(fields=['created_at'], name='destination_created_cc4833_idx'), models.Index(fields=['is_featured'], name='destination_is_feat_54f559_idx')],
            },
        ),
    ]
