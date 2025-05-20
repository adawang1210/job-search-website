from django.contrib import admin
from .models import UserProfile, Skill, ReferencePerson

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'contact']
    search_fields = ['name', 'title']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ReferencePerson)
class ReferencePersonAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name'] 