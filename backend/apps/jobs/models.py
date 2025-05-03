from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)  # 職位名稱
    company = models.CharField(max_length=200)  # 公司名稱
    location = models.CharField(max_length=200)  # 工作地點
    salary = models.CharField(max_length=100)  # 薪資範圍
    description = models.TextField()  # 職位描述
    requirements = models.TextField()  # 職位要求
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間

    def __str__(self):
        return self.title 