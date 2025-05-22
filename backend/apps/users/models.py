from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('必須提供 Email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

# 關於
class User(AbstractBaseUser, PermissionsMixin):
    MALE = '男'
    FEMALE = '女'
    OTHER = '其他'
    GENDER_CHOICES = [
        (MALE, '男'),
        (FEMALE, '女'),
        (OTHER, '其他'),
    ]
    
    
    name = models.CharField(max_length=150, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年齡', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性別', null=True, blank=True)
    highest_education = models.CharField(max_length=100, verbose_name='最高學歷', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='手機', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='信箱')
    city = models.CharField(max_length=10, verbose_name='城市', null=True, blank=True)
    district = models.CharField(max_length=10, verbose_name='地區', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='完整地址', null=True, blank=True)
    languages = models.CharField(max_length=200, verbose_name='語言能力', null=True, blank=True)
    introduction = models.TextField(blank=True, verbose_name='個人簡介', null=True)
    
    # 系統相關
    password = models.CharField(max_length=128, verbose_name='密碼', default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "用戶"
        verbose_name_plural = "用戶"

    def __str__(self):
        return f"{self.name} ({self.age}歲)" if self.age else self.name

    def get_full_address(self):
        if all([self.city, self.district, self.address]):
            return f"{self.city}{self.district}{self.address}"
        return ""

#技能包
class UserSkillPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_packages')
    name = models.CharField(max_length=100, verbose_name='技能包名稱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = "用戶技能包"
        verbose_name_plural = "用戶技能包"

    def __str__(self):
        return f"{self.user.name} - {self.name}"

#技能
class UserSkill(models.Model):
    skill_package = models.ForeignKey(UserSkillPackage, on_delete=models.CASCADE, related_name='skills', verbose_name='所屬技能包', null=True, blank=True)
    skill = models.CharField(max_length=100, verbose_name='技能名稱')
    proficiency = models.IntegerField(default=0, verbose_name='熟練度')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills', null=True, blank=True)  # 保留用户字段用于迁移
    
    class Meta:
        verbose_name = "用戶技能"
        verbose_name_plural = "用戶技能"

    def __str__(self):
        if self.skill_package:
            return f"{self.skill_package.name} - {self.skill}"
        return f"{self.user.name if self.user else 'Unknown'} - {self.skill}"

class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=100, verbose_name='學校名稱')
    major = models.CharField(max_length=100, verbose_name='科系名稱')
    degree = models.CharField(max_length=100, verbose_name='學位')
    start_date = models.DateField(verbose_name='開始日期')
    end_date = models.DateField(verbose_name='結束日期')
    description = models.TextField(verbose_name='描述')

    class Meta:
        verbose_name = "教育經歷"
        verbose_name_plural = "教育經歷"
        ordering = ['-end_date']

    def __str__(self):
        return f"{self.user.name} - {self.school} {self.major}"

# 工作經歷
class UserWorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=100, verbose_name='公司名稱')
    title = models.CharField(max_length=100, verbose_name='職稱')
    start_date = models.DateField(verbose_name='開始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='結束日期')
    description = models.TextField(verbose_name='工作描述')
    
    class Meta:
        verbose_name = "工作經歷"
        verbose_name_plural = "工作經歷"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.name} - {self.title} at {self.company}"

#我的專案
class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, verbose_name='專案名稱')
    cover_photo = models.ImageField(upload_to='project_covers/', blank=True, verbose_name='封面圖片')

    class Meta:
        verbose_name = "專案經歷"
        verbose_name_plural = "專案經歷"

    def __str__(self):
        return f"{self.user.name} - {self.title}"
    
#已按讚

#已追蹤




