# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Destination
from .forms import DestinationForm

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destination_detail.html', {'destination': destination})

def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.created_by = request.user  # Set the user who created the destination
            destination.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    return render(request, 'destination_form.html', {'form': form})

def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_detail', pk=destination.pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destination_form.html', {'form': form})

def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('destination_list')
    return render(request, 'destination_confirm_delete.html', {'destination': destination})