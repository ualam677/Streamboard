from rest_framework import serializers
from .models import Streamboard

class StreamboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streamboard
        fields = ['id', 'user', 'title', 'background_image', 'layout_json', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        streamboard = Streamboard.objects.create(user=user, **validated_data)
        return streamboard
