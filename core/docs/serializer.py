from rest_framework import serializers
from core.docs.models import Document
from core.user.serializer import UserSerializer

class DocumentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['uuid', 'title', 'content', 'created_at', 'updated_at', 'send_to', 'created_by']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            'send_to': {'required': False, 'allow_blank': True},
        }