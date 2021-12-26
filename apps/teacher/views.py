import hashlib
import re

import xlrd
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
import time
import logging
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from paper.models import Paper, QuestionBank, Exam, Subject
from paper.models import CreatePaper as cp
from student.models import Student
from teacher.models import Teacher

logger = logging.getLogger('log')


class Index(View):
    """教师首页

    """

    def get(self, request):
        keyword = request.GET.get('keyword', '')
        teacher_no = request.session.get('login_no')
        teacher_info = Teacher.objects.filter(tea_no=teacher_no).first()

        subject = Subject.objects.all()
        if keyword:
            paper_list = Paper.objects.filter(Q(title__contains=keyword) | Q(paper_no__contains=keyword)).all()
        else:
            paper_list = Paper.objects.filter(teacher__tea_no=teacher_info.tea_no).all()
        logger.info('{}请求教师主页------{}'.format(teacher_info.name, time.strftime("%Y-%m-%d %H:%M:%S")))
        return render(request, 'teacher/index.html', locals())


def paper(request, paper_no):
    """试卷对应试题"""
    if paper_no:
        paper = cp.objects.filter(paper_no__paper_no=paper_no).all()
        question_list = []
        for p in paper:
            question_list.append(p.question_no)
        return render(request, 'teacher/paper.html', locals())


class CreatePaper(View):
    """教师从题库选题组成试卷

    """

    def get(self, request):
        paper_name = request.GET.get('paper_name', '')
        subject = request.GET.get('subject', '')
        if all((paper_name, subject)):
            paper_name = '[' + time.strftime("%Y%m%d", time.localtime()) + ']' + paper_name
            question_list = QuestionBank.objects.filter(subject_id=subject).all()
            return render(request, 'teacher/create_paper.html', locals())
        else:
            return redirect('/teacher/index')

    def post(self, request):
        subject = request.POST.get('subject', '')
        paper_name = request.POST.get('paper_name', '')
        time = request.POST.get('time', '')
        duration = request.POST.get('duration', '')
        questions = request.POST.getlist('questions', '')
        if all((subject, paper_name, time, duration, questions)):
            # 教师信息
            teacher_no = request.session.get('login_no')
            teacher_info = Teacher.objects.filter(tea_no=teacher_no).first()
            # 科目信息
            subject_info = Subject.objects.get(pk=subject)

            # 创建一张试卷,前端传值 [2020210628]试卷名
            paper_name = paper_name.split('[')[1].split(']')
            paper_no = paper_name[0]
            title = paper_name[1]
            paper = Paper(paper_no=paper_no, title=title, teacher=teacher_info, subject=subject_info, time=time,
                          duration=duration)
            paper.save()

            # 试题绑定试卷
            for q in questions:
                question = QuestionBank.objects.get(pk=q)
                if question:
                    cp.objects.update_or_create(paper_no=paper, question_no=question)
            return JsonResponse({'status': 'ok', 'msg': 'ok'})
        else:
            return JsonResponse({'status': 'fail', 'msg': 'error'})


class Grade(View):
    def get(self, request):
        # 查询到该教师所有的试卷
        teacher_no = request.session.get('login_no')
        teacher_info = Teacher.objects.filter(tea_no=teacher_no).first()
        paper_list = Paper.objects.filter(teacher__tea_no=teacher_no).all()
        subject = Subject.objects.all()
        stu_list = []
        if paper_list:
            # 查看哪张试卷，初始为查询试卷的结果的第一张
            paper_id = request.GET.get('paper_id', paper_list[0].paper_no)
            # 找到考过这张试卷的所有学生
            stu_list = Exam.objects.filter(paper_no__paper_no=paper_id).order_by('-grade').all()

        return render(request, 'teacher/data.html', locals())


def stu_list(paper_id):
    stu_list = Exam.objects.filter(Q(paper_no__paper_no=paper_id) & Q(is_finish=True)) \
        .values('grade') \
        .annotate(num=Count('grade')) \
        .order_by('grade')
    grade = []
    num = []
    for s in stu_list:
        grade.append(s['grade'])
        num.append(s['num'])
    return grade, num


def grade_bar(request, paper_id):
    grade, num = stu_list(paper_id)

    c = (
        Bar(init_opts=opts.InitOpts(width='260px', height='300px'))
            .add_xaxis(grade)
            .add_yaxis("人数", num)
            .set_global_opts(title_opts=opts.TitleOpts(title="成绩分布"))
    )
    return HttpResponse(c.render_embed())


fn = """
    function(params) {
        if(params.name == '不及格')
            return '\\n\\n\\n' + params.name + ' : ' + params.value + '%';
        return params.name + ' : ' + params.value + '%';
    }
    """


def new_label_opts():
    return opts.LabelOpts(formatter=JsCode(fn), position="center")


def grade_pie(request, paper_id):
    grade, num = stu_list(paper_id)
    pass_grade = 0
    dispass_grade = 0
    for i in range(0, len(grade)):
        if grade[i] >= 60:
            pass_grade += num[i]
        else:
            dispass_grade += num[i]
    pie = Pie(init_opts=opts.InitOpts(width='250px', height='300px'))
    pie.add(
        "",
        [['及格', pass_grade], ['不及格', dispass_grade]],
        radius=[60, 80],
        label_opts=new_label_opts(),
    )
    return HttpResponse(pie.render_embed())


def re_search(search_type, text):
    if search_type == 'phone':
        pat = re.compile(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    elif search_type == 'email':
        pat = re.compile(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
    return re.search(pat, text)


def c_phone(request):
    phone = request.POST.get('phone', '')
    if not phone:
        return JsonResponse({'status': 'fail', 'msg': '请输入手机号'})
    # 验证手机号格式
    res = re_search('phone', phone)
    if not res:
        return JsonResponse({'status': 'fail', 'msg': '请输入正确的手机号'})

    # 查找教师
    tea_no = request.session['login_no']
    teacher_info = Teacher.objects.filter(tea_no=tea_no).first()
    if teacher_info.phone:
        if phone == teacher_info.phone:
            return JsonResponse({'status': 'fail', 'msg': '与原手机号相同'})
    teacher_info.phone = phone
    teacher_info.save()
    return JsonResponse({'status': 'ok', 'msg': ''})


def c_pass(request):
    password = request.POST.get('password', '')
    if not password or len(password) < 6:
        return JsonResponse({'status': 'fail', 'msg': '请输入密码，且长度大于六位'})

    # 查找教师
    tea_no = request.session['login_no']
    teacher_info = Teacher.objects.filter(tea_no=tea_no).first()
    if hashlib.sha1(password.encode('utf-8')).hexdigest() == teacher_info.password:
        return JsonResponse({'status': 'fail', 'msg': '与原密码相同'})
    teacher_info.password = password
    teacher_info.save()
    return JsonResponse({'status': 'ok', 'msg': ''})


def stu_file(request):
    # 批量导入考试学生
    f = request.FILES.get('stu_list', '')
    paper_no = request.POST.get('paper_no', '')
    # 试卷
    exam_paper = Paper.objects.filter(paper_no=paper_no).first()
    if not all((f, paper_no)):
        return JsonResponse({'status': 'fail', 'msg': '信息不完整'})
    file_suffix = f.name.split('.')[1]  # 文件后缀
    if file_suffix not in ['xls', 'xlsx']:
        return JsonResponse({'status': 'fail', 'msg': '文件类型不支持，仅支持xls\\xlsx'})
    excel = xlrd.open_workbook(filename=None, file_contents=f.read())
    student_list = excel.sheets()[0]
    n_rows = student_list.nrows
    try:
        for i in range(2, n_rows):
            stu_info = student_list.row_values(i)
            stu = Student.objects.get_or_create(stu_no=str(int(stu_info[4])), name=stu_info[3],
                                                password='000000', gender=stu_info[5],
                                                dept=stu_info[0], major=stu_info[1], cls=stu_info[2],
                                                phone='', email='')
            Exam.objects.get_or_create(stu_no=stu[0], paper_no=exam_paper)
        return JsonResponse({'status': 'ok', 'msg': ''})
    except Exception as e:
        logger.error('导入考试学生信息错误{}---{}'.format(e, time.strftime("%Y-%m-%d %H:%M:%S")))
        return JsonResponse({'status': 'fail', 'msg': '导入失败'})
