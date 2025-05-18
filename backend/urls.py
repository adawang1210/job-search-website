"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="求職網站 API",
      default_version='v1',
      description="求職網站的 API 文檔",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# 後端api url
urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),  # 根路径重定向到 swagger
    path('admin/', admin.site.urls),
    path('api/jobs/', include('backend.apps.jobs.urls')),  # 職位相關 API
    path('api/companies/', include('backend.apps.companies.urls')),  # 公司相關 API
    path('api/users/', include('backend.apps.users.urls')),  # 用戶相關 API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
