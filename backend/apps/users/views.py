from django.shortcuts import render

from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, UserSkill, UserEducation, UserWorkExperience, UserProject, UserSkillPackage
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserDetailSerializer, UserCreateUpdateSerializer,
    UserSkillSerializer, UserEducationSerializer,
    UserWorkExperienceSerializer, UserProjectSerializer,
    UserRegisterSerializer, UserLoginSerializer,
    UserSkillPackageSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView  
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import authenticate

# 註冊
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

# 登入
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 登出（加入黑名單）
class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        return [AllowAny()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserDetailSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserDetailSerializer(user).data
                })
            return Response(
                {'error': '邮箱或密码错误'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserDetailSerializer

    @action(detail=True, methods=['post'])
    def add_skill(self, request, pk=None):
        user = self.get_object()
        serializer = UserSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_education(self, request, pk=None):
        user = self.get_object()
        serializer = UserEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_work_experience(self, request, pk=None):
        user = self.get_object()
        serializer = UserWorkExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_project(self, request, pk=None):
        user = self.get_object()
        serializer = UserProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    permission_classes = [AllowAny]

class UserEducationViewSet(viewsets.ModelViewSet):
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer
    permission_classes = [AllowAny]

class UserWorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = UserWorkExperience.objects.all()
    serializer_class = UserWorkExperienceSerializer
    permission_classes = [AllowAny]

class UserProjectViewSet(viewsets.ModelViewSet):
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer
    permission_classes = [AllowAny]

class UserSkillPackageViewSet(viewsets.ModelViewSet):
    queryset = UserSkillPackage.objects.all()
    serializer_class = UserSkillPackageSerializer
    permission_classes = [AllowAny]