import logging

import xlrd
from django.contrib.admin import ModelAdmin
from django.http import JsonResponse

import xadmin
from paper.models import QuestionBank, Paper, CreatePaper, Exam, Subject

# Register your models here.

logger = logging.getLogger('log')


class QuestionBankAdmin:
    list_display = [
        'id',
        'subject', 'title', 'option_a',
        'option_b', 'option_c', 'option_d',
        'answer', 'level', 'score'
    ]
    search_fields = ['subject']
    list_filter = ['subject']
    model_icon = 'fa fa-book'
    import_excel = True

    def post(self, request, *args, **kwargs):
        f = request.FILES.get('excel', '')
        if f:
            excel = xlrd.open_workbook(filename=None, file_contents=f.read())
            question_list = excel.sheets()[0]
            n_rows = question_list.nrows
            try:
                for i in range(2, n_rows):
                    question_info = question_list.row_values(i)
                    subject = Subject.objects.get(pk=question_info[0])
                    question = QuestionBank.objects.get_or_create(subject=subject, title=question_info[1],
                                                                  option_a=question_info[2], option_b=question_info[3],
                                                                  option_c=question_info[4], option_d=question_info[5],
                                                                  answer=question_info[6],
                                                                  level=str(int(question_info[7])))
            except Exception as e:
                logger.error('导入试题错误{}'.format(e))
        return super(QuestionBankAdmin, self).post(request, args, kwargs)


class PaperAdmin:
    list_display = ['paper_no', 'title', 'teacher',
                    'subject', 'time', 'duration'
                    ]
    list_filter = ['paper_no', 'title', 'teacher', 'subject', 'time']
    search_filter = ['title', 'paper_no', 'teacher', 'subject', 'time']
    model_icon = 'fa fa-tasks'


class CreatePaperAdmin:
    list_display = [
        'paper_no', 'question_no'
    ]
    model_icon = 'fa fa-edit'


class ExamAdmin:
    list_display = [
        'paper_no', 'stu_no', 'grade'
    ]
    model_icon = 'fa fa-pencil'


class SubjectAdmin:
    list_display = ['id', 'name']
    model_icon = 'fa fa-suitcase'


xadmin.site.register(QuestionBank, QuestionBankAdmin)
xadmin.site.register(Paper, PaperAdmin)
xadmin.site.register(CreatePaper, CreatePaperAdmin)
xadmin.site.register(Exam, ExamAdmin)
xadmin.site.register(Subject, SubjectAdmin)
