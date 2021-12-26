from django import forms
from .models import Student

class UserLoginForms(forms.Form):
    stu_no = forms.CharField(required=True, min_length=10, max_length=20,
                             error_messages={
                                 'required': '请填写账号',
                                 'min_length': '至少为10位',
                                 'max_length': '最多20位'
                             })
    password = forms.CharField(required=True, min_length=6, max_length=100,
                               error_messages={
                                 'required': '请填写密码',
                                 'min_length': '至少为6位',
                                 'max_length': '最多100位'
                               })


class ChangePassword(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=100,
                               error_messages={
                                   'required': '请填写密码',
                                   'min_length': '至少为6位',
                                   'max_length': '最多100位'
                               })
