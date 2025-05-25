from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action # 新增 action
from rest_framework.response import Response # 新增 Response
from rest_framework.permissions import IsAuthenticated # 新增 IsAuthenticated (假設收藏需要使用者登入)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobOpening
from .serializers import JobOpeningSerializer
# from django.conf import settings # 如果您直接引用 User 模型，可能不需要，但如果是 settings.AUTH_USER_MODEL 則需要

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
    
    # --- 新增以下 like 和 unlike actions ---

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        收藏一個職缺 (需要使用者登入)
        前端呼叫路徑: POST /api/jobs/{pk}/like/
        """
        try:
            job = self.get_object()  # pk (職缺ID) 會自動傳入並獲取對應的 JobOpening 物件
            user = request.user

            # --- 核心收藏邏輯 ---
            # 假設您的 JobOpening 模型有一個名為 `liked_by` 的 ManyToManyField 指向使用者模型
            # 如果沒有，您需要先在 JobOpening 模型中定義它。
            # 例如: liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_job_openings', blank=True)

            if not hasattr(job, 'liked_by'):
                return Response(
                    {'error': 'JobOpening model does not have "liked_by" attribute for liking functionality.'},
                    status=status.HTTP_501_NOT_IMPLEMENTED # 501 Not Implemented
                )

            if user in job.liked_by.all():
                return Response(
                    {'status': 'already_liked', 'message': f'您已經收藏過職缺 "{job.title}"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job.liked_by.add(user)
            # job.save() # ManyToManyField 的 add/remove 會自動儲存關聯，通常不需要再呼叫 save()，除非您有其他欄位修改

            return Response(
                {'status': 'job_liked', 'message': f'職缺 "{job.title}" 已成功收藏'},
                status=status.HTTP_200_OK
            )
        except JobOpening.DoesNotExist: # 確保捕捉的是 JobOpening.DoesNotExist
            return Response({'error': '職缺不存在 (JobOpening not found).'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # 開發時可以印出詳細錯誤，生產環境應記錄到日誌
            print(f"Error in like action: {str(e)}")
            return Response({'error': '處理收藏請求時發生錯誤 (An unexpected error occurred).'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    # @swagger_auto_schema(...) # 同樣可以為 unlike 加入 swagger 描述
    def unlike(self, request, pk=None):
        """
        取消收藏一個職缺 (需要使用者登入)
        前端呼叫路徑: POST /api/jobs/{pk}/unlike/
        """
        try:
            job = self.get_object()
            user = request.user

            if not hasattr(job, 'liked_by'):
                return Response(
                    {'error': 'JobOpening model does not have "liked_by" attribute for unliking functionality.'},
                    status=status.HTTP_501_NOT_IMPLEMENTED
                )

            if user not in job.liked_by.all():
                return Response(
                    {'status': 'not_liked_yet', 'message': f'您尚未收藏職缺 "{job.title}"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job.liked_by.remove(user)

            return Response(
                {'status': 'job_unliked', 'message': f'職缺 "{job.title}" 已取消收藏'},
                status=status.HTTP_200_OK
            )
        except JobOpening.DoesNotExist:
            return Response({'error': '職缺不存在 (JobOpening not found).'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in unlike action: {str(e)}")
            return Response({'error': '處理取消收藏請求時發生錯誤 (An unexpected error occurred).'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)