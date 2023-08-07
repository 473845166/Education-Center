import datetime
import random
import re
import sys

import requests
from django.contrib.auth import logout, login, authenticate
from django.core import serializers
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import date
from django.contrib.auth.decorators import login_required

from app1.aliyun import Sample
from app1.models import CustomUser, Reserve, Openness, Record


# Create your views here.

# 发送验证码
def seed_sms(request):
    if re.match(r'^1[3-9]\d{9}$', eval(request.body)['phone']):
        code = str(random.randint(100000, 999999))
        request.session['code'] = code
        Sample.main(eval(request.body)['phone'], code, sys.argv[1:])
        return JsonResponse({'code': '1'})
    else:
        return JsonResponse({'code': '0'})


# 登录
def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('user_index'))  # 用户已登录，重定向到主页
    if request.method == "POST":
        try:
            print(request.session['code'])
        except:
            return JsonResponse({'code': '0', 'mgs': '先获取验证码'})
        if request.session['code'] == eval(request.body)['sms']:
            try:
                user = CustomUser.objects.get(telephone_number=eval(request.body)['phone'])
            except:
                user = CustomUser.objects.create(telephone_number=eval(request.body)['phone'])
            login(request, user)
            return JsonResponse({'code': '1'})
        else:
            return JsonResponse({'code': '0', 'mgs': '登录失败，验证错误'})
    return render(request, 'app1/login.html')


@login_required(login_url='user_login')
def index(request):
    my_info = serializers.serialize('json', CustomUser.objects.filter(pk=request.user.pk))
    current_time = datetime.datetime.now().time()
    current_date = datetime.datetime.now().date()
    # 新用户需要填写信息。如果已经绑定则直接提示相关信息
    if not request.user.is_superuser:
        if CustomUser.objects.get(id=request.user.id).name is None:
            return redirect(reverse('up_data'))
    sl = Reserve.objects.filter(end_time__gte=date.today())
    record = Record.objects.filter(user=request.user).values('openness__reserve', 'openness__pk', 'pk')
    serialized_events = serializers.serialize('json', sl)
    if request.method == 'POST':
        try:
            eval(request.body)['checked']
        except:
            return JsonResponse({'mgs': '请选择时间段'})
        try:
            eval(request.body)['digit']
        except:
            return JsonResponse({'mgs': '请输入人数'})
        if CustomUser.objects.get(username=request.user.username).company is None:
            return HttpResponseBadRequest('请在资料修改公司')
        res = Openness.objects.filter(pk=eval(request.body)['checked']).values()[0]
        ent = Reserve.objects.filter(id=res['reserve_id']).values()[0]
        # 事件时间线
        if current_date <= ent['start_time']:
            return HttpResponseBadRequest('没到开放时间')
        if current_date >= ent['end_time']:
            return HttpResponseBadRequest('没到开放时间')
        # 开放时段
        # if current_time <= res['start_time']:
        #     return HttpResponseBadRequest('没到开放时间')
        # if current_time >= res['end_time']:
        #     return HttpResponseBadRequest('没到开放时间')
        # 限制最大单位数
        max_total_user_count = Openness.objects.get(pk=eval(request.body)['checked']).max_company
        # 限制最大人数
        max_total_person_count = Openness.objects.get(pk=eval(request.body)['checked']).max_person
        # 已经预约最大人数
        total_person_count = Record.objects.filter(openness__id=res['id']).aggregate(total_count=Sum('count_person'))[
            'total_count'] if Record.objects.filter(openness__id=res['id']).aggregate(total_count=Sum('count_person'))[
            'total_count'] is not None else 0
        if total_person_count+int(eval(request.body)['digit']) > max_total_person_count:
            return HttpResponseBadRequest('人数上限')
        # 已经预约最大单位数
        total_user_count = len(Record.objects.filter(openness__id=res['id']))
        if total_user_count+1 > max_total_user_count:
            return HttpResponseBadRequest('单位数上限')
        date_obj = datetime.datetime.strptime(eval(request.body)['submit_date'], "%Y/%m/%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        if Record.objects.filter(openness__id=res['id'], user=request.user,
                                 submit_date=formatted_date).exists():
            return JsonResponse({'mgs': '已经预约过该时段的事件了'})
        Record.objects.create(openness_id=res['id'], user=request.user,
                              submit_date=formatted_date, count_person=eval(request.body)['digit'])
        return JsonResponse({'mgs': '预约成功'})
    data = eval(serialized_events)
    for i in data:
        if i['fields']['start_time'] <= str(current_date) <= i['fields']['end_time']:
            i['status'] = '1'
        else:
            i['status'] = '0'
    record = list(record)
    # 已经预约的排序
    myrecord = Record.objects.filter(user=request.user, submit_date__gte=timezone.now()) \
        .values('pk', 'openness__reserve__event')
    return render(request, 'app1/base2.html',
                  {'sl': data, 'record': record, 'myrecord': list(myrecord), 'my_info': my_info})


# 已经预约
@login_required(login_url='user_login')
def get_record(request):
    if request.method == 'PUT':
        Record.objects.filter(id=eval(request.body)).update(status=True)
        return JsonResponse({'mgs': '取消成功'})
    sl = Record.objects.filter(id=eval(request.body)).values('openness__reserve__event', 'user__name', 'user__company',
                                                             'user__telephone_number', 'submit_date', 'pk', 'status',
                                                             'openness__end_time', 'openness__start_time',
                                                             'submit_date', 'count_person')
    sl = list(sl)
    return JsonResponse({'info': list(sl)})


# 查询
@login_required(login_url='user_login')
def get_model(request):
    sl = Openness.objects.filter(reserve=eval(request.body)['id'])
    serialized_events = serializers.serialize('json', sl)
    return JsonResponse(
        {'data': eval(serialized_events), 'company': CustomUser.objects.get(username=request.user.username).company},
        safe=False)


# 退出
def logout_view(request):
    # 执行退出逻辑
    logout(request)
    # 其他逻辑或重定向
    return redirect(reverse('user_login'))


# 修改信息
def up_data(request):
    if request.method == 'PUT':
        CustomUser.objects.filter(username=request.user).update(**eval(request.body))
    return render(request, 'app1/up_data.html')
