from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import Destination
from .serializers import DestinationSerializer
from .permissions import IsOwnerOrReadOnly

class DestinationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        
        # Search functionality
        if search := params.get('q'):
            queryset = queryset.filter(
                Q(place_name__icontains=search) |
                Q(description__icontains=search) |
                Q(state__icontains=search)
            )
            
        # State filter
        if state := params.get('state'):
            queryset = queryset.filter(state__iexact=state)
            
        # Sorting
        return queryset.order_by(params.get('sort', '-created_at'))

class DestinationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ToggleFavoriteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        user = request.user

        if destination.favorited_by.filter(id=user.id).exists():
            destination.favorited_by.remove(user)
            return Response({'status': 'removed from favorites'}, status=status.HTTP_200_OK)
        else:
            destination.favorited_by.add(user)
            return Response({'status': 'added to favorites'}, status=status.HTTP_200_OK)