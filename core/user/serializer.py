from rest_framework import serializers
from core.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'birthdate', 'my_email_password']
        read_only_fields = ['uuid']
        extra_kwargs = {
            'my_email_password': {'write_only': True},
        }