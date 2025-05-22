from django.db import models

# Create your models here.
class User(models.Model):

    MALE = '男性'
    FEMALE = '女性'
    OTHER = '其他'
    GENDER_CHOICES = [
        (MALE, '男性'),
        (FEMALE, '女性'),
        (OTHER, '其他'),
    ]
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES) 
    highest_education = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=10) 
    district = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    
    # first_name = models.CharField(max_length=30, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.name} 技能： {self.skill}"

class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.user.name} 學歷 {self.school}{self.major}{self.degree}"
    
class UserWorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences')
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.user.name} 工作經歷 {self.title}"
    
class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    cover_photo = models.FileField(upload_to='project_cover_photo/')
    # start_date = models.DateField()
    # end_date = models.DateField()
    # content = models.TextField()

    def __str__(self):
        return f"{self.user.name} 專案經歷 {self.title}"