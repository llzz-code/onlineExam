import xlrd

import xadmin
from teacher.models import Teacher
import logging

logger = logging.getLogger('log')

# Register your models here.

class TeacherAdmin:
    list_display = ['tea_no', 'name', 'gender', 'phone']
    search_fields = ['tea_no', 'name']
    list_filter = ['gender']
    model_icon = 'fa fa-rocket'
    import_excel = True

    def post(self, request, *args, **kwargs):
        f = request.FILES.get('excel', '')
        if f:
            excel = xlrd.open_workbook(filename=None, file_contents=f.read())
            teacher_list = excel.sheets()[0]
            n_rows = teacher_list.nrows
            try:
                for i in range(2, n_rows):
                    teacher_info = teacher_list.row_values(i)
                    Teacher.objects.get_or_create(tea_no=teacher_info[0], name=teacher_info[1], password='000000',
                                                  gender=teacher_info[2], phone=teacher_info[3])
            except Exception as e:
                logger.error('导入教师错误{}'.format(e))
        return super(TeacherAdmin, self).post(request, args, kwargs)


xadmin.site.register(Teacher, TeacherAdmin)
