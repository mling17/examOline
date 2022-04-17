from django.shortcuts import render
from django import forms


# from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    name = forms.CharField(label='用户名', required=True)
    email = forms.EmailField(label='邮箱', required=True)
    password = forms.CharField(label='密码', required=True, min_length=5)
    password_confirm = forms.CharField(label='确认密码', required=True, min_length=5)

    # captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

    def is_valid(self):
        if self.is_bound:
            if self.data['password'] != self.data['password_confirm']:
                self.add_error("password_confirm", u"密码不一致")
        return super(RegisterForm, self).is_valid()


# Create your views here.
def register(request):
    form = RegisterForm()
    if request.method == 'GET':
        return render(request, 'register.html', context={'form': form})
