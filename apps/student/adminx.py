import xlrd

import xadmin
from student.models import Student
import logging
from xadmin import views


logger = logging.getLogger('log')


# Register your models here.

class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '后台管理系统'
    site_footer = 'lz站长'
    menu_style = 'accordion'


class StudentAdmin:
    list_display = ['stu_no', 'name', 'gender',
                    'dept', 'major', 'cls',
                    'phone']
    search_fields = ['stu_no', 'name']
    list_filter = ['gender', 'major', 'dept']
    import_excel = True
    model_icon = 'fa fa-fighter-jet'

    def post(self, request, *args, **kwargs):
        f = request.FILES.get('excel', '')
        if f:
            excel = xlrd.open_workbook(filename=None, file_contents=f.read())
            student_list = excel.sheets()[0]
            n_rows = student_list.nrows
            try:
                for i in range(2, n_rows):
                    student_info = student_list.row_values(i)
                    Student.objects.get_or_create(dept=student_info[0], major=student_info[1], cls=student_info[2],
                                                  name=student_info[3], stu_no=str(int(student_info[4])),
                                                  gender=student_info[5], password='000000')
            except Exception as e:
                logger.error('导入学生错误{}'.format(e))
        return super(StudentAdmin, self).post(request, args, kwargs)


xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)