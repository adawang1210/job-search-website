from django.shortcuts import render
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobOpening
from .serializers import JobOpeningSerializer
# Create your views here.

class JobOpeningViewSet(viewsets.ReadOnlyModelViewSet):
    """
    職位列表接口
    
    list:
    獲取所有職位列表
    
    retrieve:
    獲取單個職位詳情
    """
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer

    @swagger_auto_schema(
        operation_summary="獲取職位列表",
        operation_description="返回所有可用的職位列表",
        responses={200: JobOpeningSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="獲取職位詳情",
        operation_description="根據 ID 返回單個職位的詳細信息",
        responses={200: JobOpeningSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)