from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email,username,phone,password,**other):
        other.setdefault("is_staff",True)
        other.setdefault("is_superuser",True)
        other.setdefault("is_active",True)


        if other.get("is_staff") is not True:
            raise ValueError(
                'superuser must be assigned to is_staff = True'
            )
        
        if other.get("is_superuser") is not True:
            raise ValueError(
                'superuser must be assigned to is_superuser = True'
            )
        return self.create_user(email,username,phone,password,**other)
    
    def create_user(self,email,username,phone,password,**other):
        if not email:
            raise ValueError("You must provide an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,phone=phone,**other)

        user.set_password(password)
        user.save()
        return user
    
class NewUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"),unique=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=10,blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    profile= models.ImageField('/uploads',blank=True,null=True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",'phone']

    def __str__(self):
        return self.username