from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class CustomUser(models.Model):
#     username = models.CharField(max_length=64, verbose_name='아이디', unique=True)
#     email = models.EmailField(max_length=128, verbose_name='이메일')
#     password = models.CharField(max_length=64, verbose_name='비밀번호')
#     registered = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
#     active = models.BooleanField(default=False)
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name = 'Custom User'
#         verbose_name_plural = 'Custom User'