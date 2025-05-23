from rest_framework import serializers
from .models import JobOpening, JobOpeningBenefit
from apps.companies.models import Company, CompanyMedia

class JobOpeningBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpeningBenefit
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name'] 

class JobOpeningSerializer(serializers.ModelSerializer):
    company = CompanySerializer()  # Nested serializer
    benefits = JobOpeningBenefitSerializer(many=True, read_only=True)
    company_logo = serializers.SerializerMethodField()
    class Meta:
        model = JobOpening
        fields = '__all__'

    def get_company_logo(self, obj):
        try:
            return obj.company.media.logo.url  # 回傳 logo 的 URL
        except:
            return None

     