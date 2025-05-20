from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ReferencePerson, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

#已追蹤
class FollowedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferencePerson
        fields = ['id', 'name', 'photo']
