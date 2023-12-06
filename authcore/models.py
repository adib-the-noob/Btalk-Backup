from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin
)
from django.core.exceptions import ValidationError
import random


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, phone_number, full_name, password, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            is_active=True,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        superUser = self.model(phone_number=phone_number, **other_fields)
        superUser.set_password(password)
        superUser.save()
        return superUser


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        null=True,
    )
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"{self.pk} - {self.full_name}"

    def save(self, *args, **kwargs):
        try:
            self.set_user_name()
            super(User, self).save(*args, **kwargs)
            old_instance = User.objects.get(pk=self.pk).profile_picture
            if old_instance != self.profile_picture:
                old_instance.delete(save=False)

            old_cover = User.objects.get(pk=self.pk).cover_photo
            if old_cover != self.cover_photo:
                old_cover.delete(save=False)
        except:
            pass
        

    def set_user_name(self):
        try:
            if not self.username:
                random_number = str(random.randint(1000, 9999))
                first_portion_name = self.full_name.split(' ')[0].lower()
                username = f"{first_portion_name}{random_number}"
                self.username = username
                
                while User.objects.filter(username=self.username).exists():
                    random_number = str(random.randint(1000, 9999))
                    self.username = f"{first_portion_name}{random_number}"    
        except:
            pass    

class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    has_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.otp}"


