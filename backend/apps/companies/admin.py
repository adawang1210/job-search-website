from django.contrib import admin

from .models import Company, CompanyBenefit, StatutoryBenefit, OtherBenefit, Contact, CompanyWebsite, CompanyMedia, CompanyPhoto

class CompanyMediaAdmin(admin.ModelAdmin):
    list_display = ['company', 'logo']
    raw_id_fields = ['company']

class CompanyPhotoAdmin(admin.ModelAdmin):
    list_display = ['media', 'photo']
    raw_id_fields = ['media']

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyBenefit)
admin.site.register(StatutoryBenefit)
admin.site.register(OtherBenefit)
admin.site.register(Contact)
admin.site.register(CompanyWebsite)
admin.site.register(CompanyMedia, CompanyMediaAdmin)
admin.site.register(CompanyPhoto, CompanyPhotoAdmin)