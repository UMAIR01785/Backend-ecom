from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None,**extra_fields):
        if not email:
            raise ValueError("email is not valid")
        
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password,**extra_fields):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )
        
        user.is_superuser=True
        
        user.is_staff=True
        

        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    first_name=models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=15)



    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    
   
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username','phone_number']



    def __str__(self):
        return f"{self.first_name}-{self.last_name}"


    


