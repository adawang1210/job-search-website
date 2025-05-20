from django.db import models
from django.core.validators import FileExtensionValidator

class Company(models.Model):
    name = models.CharField(max_length=200)        # 公司名稱
    description = models.TextField()               # 公司描述
    industry = models.CharField(max_length=100)    # 產業類別
    location = models.CharField(max_length=200)    # 公司地點
    website = models.URLField()                    # 公司網站
    logo = models.ImageField(
        upload_to='company_logos/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        null=True,
        blank=True
    )  # 公司標誌
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間

    def __str__(self):
        return self.name 