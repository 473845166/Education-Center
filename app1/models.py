from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

# 用户
class CustomUser(AbstractUser):
    # 添加自定义字段
    wx = models.JSONField(verbose_name='微信公众号', blank=True, null=True)
    name = models.CharField(verbose_name='姓名', blank=True, null=True, max_length=255)
    company = models.CharField(verbose_name='公司单位', blank=True, null=True, max_length=255)
    telephone_number = models.CharField(verbose_name='电话号码', max_length=11, blank=True, null=True)

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

    # 一个时间只能有一个事件
    def clean(self):
        overlapping_events = Reserve.objects.filter(
            start_time__lte=self.end_time,
            end_time__gte=self.start_time
        ).exclude(pk=self.pk)

        if overlapping_events.exists():
            raise ValidationError("在此时间段内已经存在一个事件。")

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"


# 开放的事件时段
class Openness(models.Model):
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name='事件')
    start_time = models.TimeField(verbose_name='开放时间')
    end_time = models.TimeField(verbose_name='结束时间')
    max_company = models.IntegerField(verbose_name='最大单位数', default=1)
    max_person = models.IntegerField(verbose_name='最大人数', default=50)

    def __str__(self):
        return f'{self.start_time}'+'到'+f'{self.end_time}'+f'的{self.reserve}'

    class Meta:
        verbose_name = "开放的事件时段"
        verbose_name_plural = "开放的事件时段"


# 预约列表
class Record(models.Model):
    openness = models.ForeignKey(Openness, on_delete=models.CASCADE, verbose_name='事件')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='用户姓名')
    submit = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    submit_date = models.DateField(verbose_name='预约日期')
    count_person = models.IntegerField(verbose_name='人数')
    status = models.BooleanField(verbose_name='已经取消', default=False, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user, '参加的', self.openness)

    class Meta:
        verbose_name = "预约列表"
        verbose_name_plural = "预约列表"
