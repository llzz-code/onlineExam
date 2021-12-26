import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser

SEX = (
    ('男', '男'),
    ('女', '女'),
)


# Create your models here.
class Teacher(models.Model):
    tea_no = models.CharField(max_length=20, verbose_name='工号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    password = models.CharField(max_length=256, verbose_name='密码')
    gender = models.CharField(max_length=4, choices=SEX, default='男', verbose_name='性别')
    phone = models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.password = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.tea_no

    class Meta:
        verbose_name = verbose_name_plural = '教师管理'
