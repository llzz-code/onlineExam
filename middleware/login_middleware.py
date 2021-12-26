from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class UserAuthMiddle(MiddlewareMixin):
    def process_request(self, request):
        """
        通过检测session中的login_no判断用户是否登录
        需要检测的页面：教师首页，教师查看成绩，教师创建试卷
                     学生首页，学生查询已考试卷，学生个人中心

        """
        need_login = ['/teacher/index/', '/teacher/grade/',
                      '/teacher/create/', '/student/index/',
                      '/student/query/', '/student/center/']
        if request.path in need_login:
            is_login = request.session.get('login_no', None)
            if not is_login:
                return HttpResponseRedirect(reverse('login:login'))
            return None
        else:
            return None


class OnlyOneUser(MiddlewareMixin):
    def process_request(self, request):
        """
        限制一个浏览器只允许一个用户登录，如果当前session中已经存在login_no，
        则根据session中的login_type重定向至指定页面
        """
        need_check = ['/', '/login/login/']
        if request.path in need_check:
            if request.session.get('login_no', None):
                login_type = request.session.get('login_type', None)
                if login_type == 'student':
                    return redirect('/student/index')
                else:
                    return redirect('/teacher/index')
            else:
                return None
        else:
            return None

