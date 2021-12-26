import hashlib
import logging

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from login.tasks import waste_time
from student.models import Student
from teacher.models import Teacher

logger = logging.getLogger('log')


class Index(View):

    def get(self, request):
        # res = waste_time.delay().get()
        return render(request, 'index.html')


class Login(View):

    def auth_login(self, request, login_type, login_no=None, password=None):
        try:
            password = hashlib.sha1(password.encode('utf-8')).hexdigest()
            print(login_no, password)
            if login_type == 'student':
                user = Student.objects.filter(Q(stu_no=login_no) & Q(password=password)).first()
            elif login_type == 'teacher':
                user = Teacher.objects.filter(Q(tea_no=login_no) & Q(password=password)).first()
            print(user)
            return user
        except Exception as e:
            logger.error('登录验证失败{}'.format(e))
            return None

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        login_no = request.POST.get('login_no', None)
        password = request.POST.get('password', None)
        login_type = request.POST.get('login_type', None)
        print(login_type)
        if all((login_no, password, login_type)):
            user = self.auth_login(request, login_type=login_type, login_no=login_no, password=password)
            if user:
                request.session['login_no'] = login_no
                request.session['login_type'] = login_type
                if login_type == 'student':
                    return JsonResponse({'status': 'ok', 'url': '/student/index'})
                else:
                    return JsonResponse({'status': 'ok', 'url': '/teacher/index'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '账号或密码错误'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '请填写完整信息'})


class Logout(View):
    def get(self, request):
        del request.session['login_no']
        del request.session['login_type']
        return redirect('/')

def phone(request):
    return render(request, 'phoneerror.html')
