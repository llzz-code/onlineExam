import hashlib

from django.db import models

# Create your models here.

SEX = (
    ('男', '男'),
    ('女', '女'),
)
DEPT = (
    ('信息工程学院', '信息工程学院'),
    ('电气与自动化学院', '电气与自动化学院'),
    ('外语外贸学院', '外语外贸学院'),
    ('理学院', '理学院'),
    ('建筑与测绘学院', '建筑与测绘学院'),
    ('机电学院', '机电学院'),
    ('经管学院', '经管学院'),
    ('马克思学院', '马克思学院')
)


class Student(models.Model):
    stu_no = models.CharField(max_length=20, verbose_name='学号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    password = models.CharField(max_length=256, verbose_name='密码')
    gender = models.CharField(max_length=4, verbose_name='性别', choices=SEX, default='男')
    dept = models.CharField(max_length=20, verbose_name='学院', choices=DEPT, default='信息工程学院')
    major = models.CharField(max_length=20, verbose_name='专业')
    cls = models.CharField(max_length=20, verbose_name='班级')
    phone = models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)
    email = models.CharField(max_length=30, verbose_name='邮箱', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.password = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.stu_no

    class Meta:
        verbose_name = verbose_name_plural = '学生管理'
