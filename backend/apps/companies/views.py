from django.shortcuts import render
from rest_framework import viewsets
from .models import Company, CompanyPhoto, CompanyMedia
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanySerializer, CompanyPhotoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CompanyMediaSerializer

# Create your views here.

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    公司信息的视图集
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @swagger_auto_schema(
        operation_summary="获取所有公司列表",
        operation_description="返回系统中所有公司的信息列表"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="获取特定公司详情",
        operation_description="根据公司ID返回特定公司的详细信息"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
class CompanyMediaViewSet(viewsets.ModelViewSet):
    queryset = CompanyMedia.objects.all()
    serializer_class = CompanyMediaSerializer
# class CompanyPhotoViewSet(APIView):
#     def get(self, request):
#         photos = CompanyPhoto.objects.all()
#         serializer = CompanyPhotoSerializer(photos, many=True, context={'request': request})
#         return Response(serializer.data)