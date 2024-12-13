from rest_framework.serializers import Serializer, EmailField, CharField, ValidationError
from users.models import CustomUser
from django.contrib.auth.hashers import make_password

class RegisterSerializer(Serializer):
    username = CharField(max_length=150, required=True)
    email = EmailField(required=True)
    password1 = CharField(write_only=True, required=True, min_length=8)
    password2 = CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password1']),
        )
        return user