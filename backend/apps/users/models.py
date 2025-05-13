from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    # 技能可以用多對多
    skills = models.ManyToManyField('Skill', blank=True)

class Skill(models.Model):
    name = models.CharField(max_length=50)

class Experience(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    description = models.TextField()

class ProjectFolder(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='project_folders')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='project_folders/', blank=True)

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='companies')

class ReferencePerson(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='reference_photos/', blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='references')
