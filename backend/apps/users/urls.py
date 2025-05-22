from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, UserSkillViewSet, UserEducationViewSet,
    UserWorkExperienceViewSet, UserProjectViewSet,
    RegisterView, CustomTokenObtainPairView, LogoutView,
    UserSkillPackageViewSet
)

router = DefaultRouter()
router.register(r'profiles', UserViewSet)
router.register(r'skills', UserSkillViewSet)
router.register(r'education', UserEducationViewSet)
router.register(r'work-experience', UserWorkExperienceViewSet)
router.register(r'projects', UserProjectViewSet)
router.register(r'skill-packages', UserSkillPackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]