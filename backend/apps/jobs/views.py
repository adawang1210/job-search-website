from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer

#這個要放在navbar
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        """
        可以根據查詢參數過濾職位
        例如：/api/jobs/?company=Google
        """
        queryset = Job.objects.all()
        company = self.request.query_params.get('company', None)
        if company:
            queryset = queryset.filter(company__icontains=company)
        return queryset 