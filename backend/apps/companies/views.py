from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        """
        可以根據產業類別過濾公司
        例如：/api/companies/?industry=科技
        """
        queryset = Company.objects.all()
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        return queryset 