from rest_framework import serializers
from ..models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'modified_at', 'favorited_by')

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and user.favorite_destinations.filter(pk=obj.pk).exists()