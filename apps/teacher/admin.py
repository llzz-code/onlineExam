from django.contrib import admin
from teacher.models import Teacher
# Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['tea_no', 'gender', 'phone']


admin.site.register(Teacher, TeacherAdmin)
