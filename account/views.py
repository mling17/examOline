import time
from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.db.models import Q
from account.forms.account import RegisterModelForm, LoginForm, ChangePasswordForm, ForgetPasswordForm
from account import models
from account.utils.image_code import check_code
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.urls import reverse
import jwt


class UserInfo(object):

    def __init__(self, user=None):
        self.user = user


def get_base_url(request):
    """
    Get base URL from the request
    """
    host = request.get_host()
    if ":" not in host:
        # tricky here: when used with nginx+uwsgi, port is not included
        host += ":" + request.get_port()
    return request.scheme + "://" + host


def make_token(data):
    d = {
        'exp': time.time() + settings.TOKEN_EXPIRE,
        'iat': time.time(),
        'iss': 'mling17',
        'data': data
    }
    return jwt.encode(d, settings.SECRET_KEY, algorithm='HS256')


def send_email(request, subject, to_email, token, type):
    """
    发送邮件
    :param request:
    :param subject:
    :param to_email:
    :param token:
    :param type: 0.注册（register）；1.修改密码（change）；2.找回密码（forget）
    :return:
    """
    from_email = settings.EMAIL_FROM  # 发件人，在settings.py中已经配置
    # 发送的消息
    message = ''  # 发送普通的消息使用的时候message
    base_url = get_base_url(request)
    if type == 'register':
        meg_html = f'<p>请点击下面的链接激活你的账号(有效时间{settings.TOKEN_EXPIRE // 3600}小时):</p><a href="{base_url}{reverse("account:email_active")}?token={token}">{base_url}{reverse("account:email_active")}?token={token}</a>'  # 发送的是一个html消息 需要指定
    elif type == 'change':
        meg_html = f'<p>请点击下面的链接修改密码(有效时间{settings.TOKEN_EXPIRE // 3600}小时):</p><a href="{base_url}{reverse("account:change_password")}?token={token}">{base_url}{reverse("account:change_password")}?token={token}</a>'  # 发送的是一个html消息 需要指定
    elif type == 'forget':
        meg_html = f'<p>请点击下面的链接重置密码(有效时间{settings.TOKEN_EXPIRE // 3600}小时):</p><a href="{base_url}{reverse("account:forget")}?token={token}">{base_url}{reverse("account:forget")}?token={token}</a>'  # 发送的是一个html消息 需要指定
    else:
        raise ValueError('type param want (register,change,forget),get %s' % type)
    send_mail(subject, message, from_email, [to_email], html_message=meg_html)
    return True


def index(request):
    return render(request, 'index.html')


def register(request):
    """注册视图"""
    if request.method == 'GET':
        form = RegisterModelForm(request)
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(request, request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        mobile_phone = form.cleaned_data.get('mobile_phone')
        nickname = password[:8]
        data = {'email': email, }
        token = make_token(data)
        send_email(request, subject='账号激活', to_email=email, token=token, type='register')
        email_obj = models.EmailVerifyRecord()
        email_obj.email = email
        email_obj.token = token
        email_obj.m_type = 0
        email_obj.save()
        user = models.User()
        user.username = username
        user.password = password
        user.email = email
        user.mobile_phone = mobile_phone
        user.nickname = nickname
        user.save()
        context = {'msg': '注册成功，请登录邮箱激活账号。', 'next_pg': None}
        return render(request, 'common_msg.html', context=context)
    return render(request, 'register.html', {'form': form})


def email_active(request):
    token = request.GET.get('token')
    try:
        record = models.EmailVerifyRecord.objects.filter(token=token, is_valid=True).first()
        if record:
            models.EmailVerifyRecord.objects.filter(token=token).update(is_valid=False)
            user = models.User.objects.filter(email=record.email).first()
            user.mail_valid = True
            user.save()
            request.session['user_id'] = user.id
            request.user_info = UserInfo(user)
            context = {'msg': '邮箱激活成功,3秒后自动跳转', 'next_pg': reverse('account:index')}
            return render(request, 'common_msg.html', context=context)
        else:
            return HttpResponse('邮箱验证错误或链接已失效')
    except jwt.exceptions.ExpiredSignatureError:
        models.EmailVerifyRecord.objects.filter(token=token).update(is_valid=False)
        return HttpResponse(mark_safe('<input type="text" name="email" placeholder="邮箱">'))  # todo token过期的情况处理


def login(request):
    """ 用户名和密码登录 """
    if request.method == 'GET':
        if request.session.get('user_id'):
            return redirect('account:index')
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_object = models.User.objects.filter(Q(username=username) | Q(mobile_phone=username) | Q(email=username)) \
            .filter(password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(settings.SESSION_EXPIRE)
            return redirect(settings.SIGNED_DIRECT)
        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect(settings.SIGNED_DIRECT)


def send_change_password_mail(request):
    email = request.user_info.user.email
    data = {'email': email, }
    token = make_token(data)
    send_email(request, '修改密码', email, token=token, type='change')
    email_user, domain = email.split('@')
    email_str = email_user[:2] + '***' + email[-1] + '@' + domain
    record_obj = models.EmailVerifyRecord(email=email, token=token, m_type=1)
    record_obj.save()
    return HttpResponse(f'修改密码链接已发送到您的邮箱：{email_str}，请点击邮箱链接进行修改。')


def change_password(request):
    if request.method == 'GET':
        form = ChangePasswordForm(request)
        token = request.GET.get('token')
        try:
            if models.EmailVerifyRecord.objects.filter(token=token, is_valid=True).exists():
                return render(request, 'change_password.html', {'form': form, 'token': token})
            raise jwt.exceptions.ExpiredSignatureError
        except jwt.exceptions.ExpiredSignatureError:
            return HttpResponse('链接已失效')
    form = ChangePasswordForm(request, request.POST)
    if form.is_valid():
        token = request.POST.get('token')
        new_pwd = form.cleaned_data.get('password')
        record_obj = models.EmailVerifyRecord.objects.filter(token=token).first()
        record_obj.is_valid = False
        record_obj.save()
        models.User.objects.filter(email=record_obj.email).update(password=new_pwd)
        context = {'next_pg': reverse('account:login'), 'msg': '密码修改成功,请重新登录'}
        request.session.flush()
        return render(request, 'common_msg.html', context=context)
    return render(request, 'change_password.html', {'form': form})


def forget(reqeust):
    if reqeust.method == 'GET':
        token = reqeust.GET.get('token')
        if token:
            record = models.EmailVerifyRecord.objects.filter(token=token, m_type=2, is_valid=True).first()
            try:
                data = jwt.decode(token, settings.SECRET_KEY, issuer='mling17', algorithms='HS256')['data']
                email = data.get('email')
                password = data.get('password')
                record.is_valid = False
                record.save()
                models.User.objects.filter(email=email).update(password=password)
                context = {'msg': '密码重置成功，请重新登录。', 'next_pg': reverse('account:login')}
                return render(reqeust, 'common_msg.html', context=context)
            except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError, AttributeError):
                return HttpResponse('链接失效')
        form = ForgetPasswordForm(reqeust)
        return render(reqeust, 'change_password.html', {'form': form})
    form = ForgetPasswordForm(reqeust, reqeust.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        data = {'email': email, 'password': password}
        token = make_token(data)
        models.EmailVerifyRecord.objects.create(email=email, token=token, m_type=2)
        send_email(reqeust, '重置密码', email, token, 'forget')
        context = {'msg': '重置密码邮件已发送，请前往邮箱点击重置链接。'}
        return render(reqeust, 'common_msg.html', context=context)
    return render(reqeust, 'change_password.html', {'form': form})


def hello(request):
    return HttpResponse('hello')
