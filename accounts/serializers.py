from rest_framework import serializers
from .models import User, OtpCode
from datetime import datetime


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=12)
    year_published = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):

    def create(self, obj, **kwargs):
        User.objects.create_user(**self.data)
        return obj

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'password', 'profile')


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'
