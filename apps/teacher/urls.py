from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from teacher.views import Index, paper, CreatePaper, Grade, grade_bar, grade_pie, c_phone, c_pass, stu_file

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    url(r'paper/(\d+)/$', paper, name='paper'),
    path('create/', CreatePaper.as_view(), name='create'),
    path('grade/', Grade.as_view(), name='grade'),
    url(r'grade_bar/(\d+)/$', grade_bar, name='grade_bar'),
    url(r'grade_pie/(\d+)/$', grade_pie, name='grade_pie'),
    path('c_phone/', c_phone, name='c_phone'),
    path('c_pass/', c_pass, name='c_pass'),
    path('file/', stu_file, name='file'),
]