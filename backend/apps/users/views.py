from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, FollowedPersonSerializer
from .models import UserProfile, ReferencePerson

class UserViewSet(viewsets.ModelViewSet):
    """
    這是一個針對使用者的視圖集，負責處理所有與使用者有關的資料操作，例如建立帳號、查詢使用者資訊、更新資料或刪除使用者。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def followed_persons(self, request, pk=None):
        """
        獲取用戶已關注的人員列表
        """
        try:
            user_profile = UserProfile.objects.get(id=pk)
            references = user_profile.references.all()
            serializer = FollowedPersonSerializer(references, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "用戶個人資料不存在"},
                status=status.HTTP_404_NOT_FOUND
            ) 