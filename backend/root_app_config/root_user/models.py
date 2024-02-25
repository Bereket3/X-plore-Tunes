from typing import Any


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
    )
from django.utils.translation import gettext_lazy as _



class AuthUserAccountManager(BaseUserManager):
    """
    Custom user manager class to create user, super users and admin users.
    """
    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('You are not a staff member')
        return self.create_user(email, username, password, **other_fields)
    
    
    def create_admin_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class AuthUserModel(AbstractBaseUser, PermissionsMixin):
    """
    Main user class model.

    Can be extended to have as many fields as desire by add or removing different fields to the user model class.
    """
    
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    gender = models.CharField(max_length=200, default="male", choices=(('male','male'), ('female','female')))
    age = models.IntegerField(default=0)
    premium_user = models.BooleanField(default=False)
    
    objects = AuthUserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        """
        when an user is deleted the profile picture also will  be deleted

        these function make sure that the profile picture exists and make sure to delete it
        """
        self.profile_picture.delete()
        return super().delete(using, keep_parents)