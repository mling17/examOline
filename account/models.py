from django.db import models


# Create your models here.
class User(models.Model):
    gender_choice = (
        (0, "男"),
        (1, "女"),
        (2, "未知")
    )
    identity_choices = (
        (0, '普通'),
        (1, '学生'),
        (2, '老师'),
        (3, '管理员'),
    )
    # uid = models.UUIDField()
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    mail_valid = models.BooleanField(verbose_name='邮箱是否激活', default=False)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=11, default='')
    nickname = models.CharField(max_length=32, verbose_name=u"昵称")
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice, default=3)
    identity = models.SmallIntegerField(verbose_name=u"角色", choices=identity_choices, default=0)
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    avatar = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    type_choice = [
        (0, '注册激活'),
        (1, '修改密码'),
        (2, '忘记密码'),
    ]
    token = models.CharField(verbose_name='token', max_length=254)
    m_type = models.SmallIntegerField(verbose_name='邮件类型', choices=type_choice)
    email = models.EmailField(verbose_name='邮箱地址')
    is_valid = models.BooleanField(verbose_name='是否可用', default=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
