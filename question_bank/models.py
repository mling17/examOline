from django.db import models
from account.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class QuestionBank(models.Model):
    # 题库
    title = models.CharField(verbose_name='标题', max_length=32)
    content = models.CharField(verbose_name='介绍', max_length=32)
    # sort_num = models.CharField(verbose_name='标题', max_length=32)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    post_state = models.BooleanField(verbose_name='发布状态', default=True)
    is_valid = models.BooleanField(verbose_name='是否可用', default=True)
    cover = models.ImageField(verbose_name='封面', upload_to='image/%Y%m', default='image/default.png', max_length=100)
    user_id = models.IntegerField(verbose_name='创建用户ID', default=0)
    subject_name = models.CharField(verbose_name='科目名', max_length=32)

    def count(self):
        num = Question.objects.filter(question_bank=self).count()
        if not num:
            return 0
        return num

    def __str__(self):
        return self.title


question_type_choice = [
    (1, '单选题'),
    (2, '多选题'),
    (3, '判断题'),
    (4, '填空题'),
    (5, '简答题'),
    (6, '综合题'),
]


class Question(models.Model):
    # 题
    question_bank = models.ForeignKey(verbose_name='关联题库', to='QuestionBank', on_delete=models.CASCADE)
    # subject_id = models.CharField(verbose_name='标题', max_length=32)
    type = models.SmallIntegerField(verbose_name='题目类型', choices=question_type_choice)
    # title = models.CharField(verbose_name='题目', max_length=512)
    title = RichTextUploadingField(verbose_name='题目', max_length=1024)
    analysis = models.TextField(verbose_name='解析', max_length=1024)
    sort_num = models.IntegerField(verbose_name='排序')
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_valid = models.BooleanField(verbose_name='是否可用', default=True)
    user_id = models.IntegerField(verbose_name='创建用户ID', default=0)

    def options(self):
        option_dict = ChoiceOptions.objects.filter(question=self).values()
        return option_dict

    def answer(self):
        res = ChoiceOptions.objects.filter(question=self, is_answer=True).values()
        return res


class ChoiceOptions(models.Model):
    # 选项
    question = models.ForeignKey(verbose_name='题目选项', to='Question', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='选项标题', max_length=8)
    content = models.CharField(verbose_name='选项内容', max_length=256)
    is_answer = models.BooleanField(verbose_name='是否是正确答案', default=False)


class ImportFile(models.Model):
    file = models.FileField(upload_to='uploads/question_dir/%Y/%m/%d/')
    name = models.CharField(max_length=50, verbose_name=u'文件名')
    user = models.ForeignKey(verbose_name='上传者', to=User, on_delete=models.CASCADE)
    ctime = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
