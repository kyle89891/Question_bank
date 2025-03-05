from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    qus = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.qus

class Option(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    

# class Answer(models.Model): 
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Update if needed
#     selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, blank=True, null=True)  # Or store answer text as a CharField

# class User(AbstractUser):
#     Country_Code        = models.CharField(max_length = 250, blank=True, default = '')
#     Phone_No            = models.CharField(max_length = 250, blank=True, null=False)
#     Company_Name        = models.CharField(max_length = 250, blank=True, default = '')
#     Designation_Name    = models.CharField(max_length = 250, blank=True, default = '')
#     Address             = models.CharField(max_length = 250, blank=True, default = '')
#     Website_url         = models.CharField(max_length = 250, blank=True, default = '')
#     Linkdin_url         = models.CharField(max_length = 250, blank=True, default = '')