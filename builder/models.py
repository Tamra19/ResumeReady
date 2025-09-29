from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=200)
    summary = models.TextField(blank=True, null=True,help_text="A brief professional summary")
    skills = models.TextField(help_text="Comma-separated list of skills (eg- Python, Django, HTML).")
    
    def __str__(self):
        return self.name
    
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current")
    description = models.TextField()
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    graduation_date = models.DateField()
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"
