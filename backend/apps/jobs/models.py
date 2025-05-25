from django.db import models
from django.conf import settings 
from apps.companies.models import Company  

class JobOpening(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_openings', null=True, blank=True)  # 職位所屬公司
    title = models.CharField(max_length=200)  
    recruitment_type = models.CharField(max_length=200)  
    experience_required  = models.CharField(max_length=150)  
    education_required = models.CharField(max_length=150) 
    major_required = models.CharField(max_length=150, null=True, blank=True) 
    salary_type = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True )  # 最低薪資
    salary_max = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # 最高薪資
    salary_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # 薪資數字 
    location = models.CharField(max_length=200)  # 工作地點
    # applicants = 
    description = models.TextField()  # 職位描述
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    # posting_date = models.DateField()  # 職位發布日期

    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # 指向 Django 設定中定義的使用者模型
        related_name='liked_job_openings', # 讓您可以從 User 模型反向查詢 user.liked_job_openings.all()
        blank=True # 表示此欄位可以為空 (也就是一個職缺一開始沒有被任何人收藏)
    )

    def __str__(self):
        return self.title

class JobOpeningBenefit(models.Model):
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='benefits')
    benefits_description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.job_opening.title} 個別福利"
 
    