from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models

class UserProfile(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('participant', 'Participant'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='participant')
    groups = models.ManyToManyField(Group, related_name='user_profiles')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles')


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    # Add any other fields you need for your questions

    def __str__(self):
        return self.question_text
    

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    # Add any other fields you need for your test cases

    def __str__(self):
        return f"Test case for {self.question}"
