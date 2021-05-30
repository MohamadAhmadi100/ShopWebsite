from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True, verbose_name='ایمیل')
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    phone = models.PositiveIntegerField(null=True, blank=True, unique=True, verbose_name='تلفن')
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال')
    is_admin = models.BooleanField(default=False, verbose_name='دسترسی ادمین')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
