import datetime
import re
import requests
from django.contrib.auth import logout, login, authenticate
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import date
from django.contrib.auth.decorators import login_required

from app1.models import CustomUser, Reserve, Openness, Record


# Create your views here.

# 发送验证码
def seed_sms(request):
    if re.match(r'^1[3-9]\d{9}$', eval(request.body)['phone']):
        return JsonResponse({'code': '1'})
    else:
        return JsonResponse({'code': '0'})


# 登录
def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('user_index'))  # 用户已登录，重定向到主页
    if request.method == "POST":
        if authenticate(**eval(request.body)):
            login(request, authenticate(**eval(request.body)))
            return JsonResponse({'code': '1'})
        else:
            return JsonResponse({'code': '0'})
    return render(request, 'app1/login.html')


@login_required(login_url='user_login')
def index(request):
    my_info=serializers.serialize('json', CustomUser.objects.filter(pk=request.user.pk))
    print(my_info)
    current_time = datetime.datetime.now().time()
    current_date = datetime.datetime.now().date()
    # 新用户需要填写信息。如果已经绑定则直接提示相关信息
    if not request.user.is_superuser:
        if CustomUser.objects.get(id=request.user.id).name is None:
            return redirect(reverse('up_data'))
    sl = Reserve.objects.filter(end_time__gte=date.today())
    record = Record.objects.filter(user=request.user).values('reserve__event', 'reserve__pk', 'pk')
    serialized_events = serializers.serialize('json', sl)
    if request.method == 'POST':
        res = Openness.objects.filter(pk=eval(request.body)['checked']).values()[0]
        ent = Reserve.objects.filter(id=res['reserve_id']).values()[0]
        # 事件时间线
        if current_date <= ent['start_time']:
            return HttpResponseBadRequest('没到开放时间')
        if current_date >= ent['end_time']:
            return HttpResponseBadRequest('没到开放时间')
        # 开放时段
        if current_time <= res['start_time']:
            return HttpResponseBadRequest('没到开放时间')
        if current_time >= res['end_time']:
            return HttpResponseBadRequest('没到开放时间')
        if Record.objects.filter(reserve_id=res['reserve_id'], user=request.user).exists():
            return JsonResponse({'mgs': '已经预约过了'})
        Record.objects.create(reserve_id=res['reserve_id'], user=request.user)
        return JsonResponse({'mgs': '预约成功'})
    data = eval(serialized_events)
    for i in data:
        if i['fields']['start_time'] <= str(current_date) <= i['fields']['end_time']:
            i['status'] = '1'
        else:
            i['status'] = '0'
    record = list(record)
    return render(request, 'app1/base2.html', {'sl': data, 'record': record,'my_info':my_info})


# 已经预约
@login_required(login_url='user_login')
def get_record(request):
    sl = Record.objects.filter(id=eval(request.body)).values('reserve__event', 'user__name', 'user__company',
                                                             'user__telephone_number','submit')
    sl = list(sl)
    return JsonResponse({'info': list(sl)})


# 查询
@login_required(login_url='user_login')
def get_model(request):
    sl = Openness.objects.filter(reserve=eval(request.body)['id'])
    serialized_events = serializers.serialize('json', sl)
    return JsonResponse(eval(serialized_events), safe=False)


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
