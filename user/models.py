from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    identity_choices = (
        (0, '普通'),
        (1, '学生'),
        (2, '老师'),
        (3, '管理员'),
    )

    name = models.CharField(max_length=32, verbose_name=u"姓名", default='')
    password = models.CharField(max_length=50, verbose_name=u"姓名", default='')
    identity = models.SmallIntegerField(verbose_name=u"角色", choices=identity_choices, default=0)
    gender = models.SmallIntegerField(verbose_name=u"性别", choices=gender_choices, default='male')
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    avatar = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)
    mail_valid = models.BooleanField(verbose_name='邮箱是否激活', default=False)
    email = models.EmailField(verbose_name='邮箱', default=False, unique=True)
    phone = models.CharField(verbose_name='手机号', default='')
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username  # 在默认数据库中


class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证码类型', choices=send_choices, max_length=10)
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
