from rest_framework import serializers
from .models import CompanyPhoto
from .models import Company, CompanyBenefit, StatutoryBenefit, OtherBenefit, Contact, CompanyWebsite, CompanyMedia, CompanyPhoto 

class StatutoryBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutoryBenefit
        fields = ['id', 'benefit']

class OtherBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBenefit
        fields = ['id', 'benefit']

class CompanyBenefitSerializer(serializers.ModelSerializer):
    statutory = StatutoryBenefitSerializer(many=True, read_only=True)
    others = OtherBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyBenefit
        fields = ['id', 'benefits_description', 'statutory', 'others']

class CompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CompanyWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWebsite
        fields = '__all__'

class CompanyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPhoto
        fields = ['id', 'photo']
    
class CompanyMediaSerializer(serializers.ModelSerializer):
    photos = CompanyPhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = CompanyMedia
        fields = ['id', 'company', 'logo', 'photos']

    def create(self, validated_data):
        company = validated_data.get('company')
        try:
            # 尝试获取现有记录
            instance = CompanyMedia.objects.get(company=company)
            # 更新 logo
            instance.logo = validated_data.get('logo')
            instance.save()
            return instance
        except CompanyMedia.DoesNotExist:
            # 如果不存在，创建新记录
            return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance

class CompanySerializer(serializers.ModelSerializer):
    benefits = CompanyBenefitSerializer(many=True, read_only=True)
    contacts = CompanyContactSerializer(many=True, read_only=True)
    websites = CompanyWebsiteSerializer(many=True, read_only=True)
    media = CompanyMediaSerializer(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'