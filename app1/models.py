from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 用户
class CustomUser(AbstractUser):
    # 添加自定义字段
    wx = models.JSONField(verbose_name='微信公众号', blank=True, null=True)
    name = models.CharField(verbose_name='姓名', blank=True, null=True, max_length=255)
    company = models.CharField(verbose_name='公司单位', blank=True, null=True, max_length=255)
    telephone_number = models.IntegerField(verbose_name='电话号码', blank=True, null=True)

    def __str__(self):
        try:
            return self.username
        except Exception as e:
            print(e)
            return ''

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


# 事件
class Reserve(models.Model):
    event = models.CharField(verbose_name='事件', max_length=255)
    start_time = models.DateField(verbose_name='开始时间')
    end_time = models.DateField(verbose_name='结束时间')

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"


# 预约列表
class Record(models.Model):
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name='事件')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='用户姓名')
    submit = models.DateTimeField(verbose_name='请求预约时间', auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user, '参加的', self.reserve)

    class Meta:
        verbose_name = "预约列表"
        verbose_name_plural = "预约列表"


# 开放的事件时段
class Openness(models.Model):
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name='事件')
    start_time = models.TimeField(verbose_name='开放时间')
    end_time = models.TimeField(verbose_name='结束时间')
    max_person = models.IntegerField(verbose_name='最大人数', default=1)

    def __str__(self):
        return '{}'.format(self.start_time, '到', self.end_time, '的事件', self.reserve)

    class Meta:
        verbose_name = "开放的事件时段"
        verbose_name_plural = "开放的事件时段"
