from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role

# Create your models here.
class User(AbstractBaseUser):
    username=models.CharField(max_length=50,unique=True)
    firstname=models.CharField(max_length=20)
    middlename=models.CharField(max_length=20,blank=True,null=True)
    lastname=models.CharField(max_length=20)
    password=models.CharField(max_length=128)
    reset_pass=models.BooleanField(blank=True,null=True,default=False)
    description=models.TextField(blank=True,null=True)
    email=models.EmailField(unique=True,max_length=50)
    roles = models.ManyToManyField(Role, related_name='users')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']
    def __str__(self):
        return self.username