from django.contrib import admin
from django.utils.safestring import mark_safe
from student.models import Student


# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['stu_no', 'gender',
                    'dept', 'major', 'cls',
                    'phone']


admin.site.register(Student, StudentAdmin)
