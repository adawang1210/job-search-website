from rest_framework.routers import DefaultRouter
from apps.companies.views import CompanyViewSet
from apps.companies.views import CompanyMediaViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', CompanyViewSet, basename='company')  # 不加 'companies'
router.register(r'media', CompanyMediaViewSet)
urlpatterns = router.urls + [
    path('', include(router.urls)),
]