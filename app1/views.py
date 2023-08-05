import requests
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.urls import reverse
from app1.models import CustomUser


# Create your views here.

def index(request):
    return render(request, 'app1/base2.html')


def user(request):
    return render(request, 'app1/user.html')


def center(request):
    return render(request, 'app1/center.html')


# 退出
def logout_view(request):
    # 执行退出逻辑
    logout(request)
    # 其他逻辑或重定向
    return redirect(reverse('user_index'))


# 修改信息
def up_data(request):
    return render(request, 'app1/up_data.html')


# 微信公众号授权
def wx(request):
    CODE = request.GET.get('code')
    code_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={SECRET}&code={CODE}&grant_type' \
               f'=authorization_code'
    response = requests.get(code_url).json()
    info_url = f'https://api.weixin.qq.com/sns/userinfo?' \
               f'access_token={response["access_token"]}&openid={response["openid"]}&lang=zh_CN'
    get_info = requests.get(info_url).json()
    get_info['nickname'] = get_info['nickname'].encode('iso-8859-1').decode('utf-8')
    try:
        user = CustomUser.objects.get(username=get_info['openid'])
    except Exception as e:
        print(e)
        user = CustomUser.objects.create_user(username=get_info['openid'], password=get_info['openid'], info1=get_info)
    login(request, user)
    if request.GET.get('state'):
        state = request.GET.get('state')
        return redirect(reverse('user_index') + f'?state={state}')
    return redirect(reverse('user_index'))

def up_wx(request):
    CODE = request.GET.get('code')
    code_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={SECRET}&code={CODE}&grant_type' \
               f'=authorization_code'
    response = requests.get(code_url).json()
    info_url = f'https://api.weixin.qq.com/sns/userinfo?' \
               f'access_token={response["access_token"]}&openid={response["openid"]}&lang=zh_CN'
    get_info = requests.get(info_url).json()
    get_info['nickname'] = get_info['nickname'].encode('iso-8859-1').decode('utf-8')
    CustomUser.objects.filter(username=request.user.username).update(wx=get_info)
    return redirect(reverse('user_index'))
