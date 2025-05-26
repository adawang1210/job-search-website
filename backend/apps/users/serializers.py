from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, ValidationError
from django.contrib.auth import authenticate
from .models import (
    User, UserSkill, UserEducation, 
    UserWorkExperience, UserProject, UserSkillPackage
)

# 自訂 Token 取得 serializer（可自定回傳內容）
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'email': self.user.email})
        return data

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'proficiency', 'icon_svg']

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = ['id', 'school', 'major', 'degree', 'start_date', 'end_date', 'description']

class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkExperience
        fields = ['id', 'user', 'company', 'title', 'start_date', 'end_date', 'description']
        extra_kwargs = {
            'user': {'write_only': True}  # user 字段只用于写入，不在响应中显示
        }

class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ['id', 'cover_photo', 'title']

class UserDetailSerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(many=True, read_only=True)
    educations = UserEducationSerializer(many=True, read_only=True)
    work_experiences = UserWorkExperienceSerializer(many=True, read_only=True)
    projects = UserProjectSerializer(many=True, read_only=True)
    full_address = serializers.CharField(source='get_full_address', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'picture', 'age', 'gender', 'highest_education', 
            'phone', 'email', 'city', 'district', 'address',
            'full_address', 'languages', 'introduction',
            'skills', 'educations', 'work_experiences', 'projects'
        ]

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 'age', 'gender', 'highest_education',
            'phone', 'email', 'city', 'district', 'address',
            'languages', 'introduction'
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("密碼不匹配")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSkillPackageSerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserSkillPackage
        fields = ['id', 'user', 'name', 'created_at', 'updated_at', 'skills']