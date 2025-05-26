from django.contrib import admin
from .models import User, UserSkill, UserEducation, UserWorkExperience, UserProject, UserSkillPackage

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'email', 'city', 'district', 'is_superuser')
    search_fields = ('name', 'email')
    list_filter = ('gender', 'city', 'is_superuser', 'is_staff')

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 3  # 默认显示3个空的技能输入框

@admin.register(UserSkillPackage)
class UserSkillPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('name',)
    inlines = [UserSkillInline]

@admin.register(UserEducation)
class UserEducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'major', 'degree', 'start_date', 'end_date')
    list_filter = ('degree', 'school')
    search_fields = ('school', 'major')

@admin.register(UserWorkExperience)
class UserWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'title', 'start_date', 'end_date')
    list_filter = ('company',)
    search_fields = ('company', 'title')

@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('title',)
    list_filter = ('user',)
