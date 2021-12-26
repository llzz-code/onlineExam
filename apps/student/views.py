from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from onlineExam.settings import WEBNAME, EMAIL_FROM
from paper.models import Exam, CreatePaper, Paper, QuestionBank
from .forms import UserLoginForms, ChangePassword
# Create your views here.
from django.views.generic.base import View
from student.models import Student


class StuIndex(View):

    def get(self, request):
        stu_no = request.session.get('login_no')
        exam_list = Exam.objects.filter(Q(stu_no__stu_no=stu_no) & Q(is_finish=False))
        return render(request, 'student/index.html', locals())


class QueryGrade(View):
    def get(self, request):

        stu_no = request.session.get('login_no')
        grade_list = Exam.objects.filter(Q(stu_no__stu_no=stu_no) & Q(is_finish=True)).all()
        if grade_list:
            return render(request, 'student/grade.html', locals())
        else:
            return render(request, 'student/grade.html', locals())


class Center(View):
    def get(self, request):

        stu_no = request.session.get('login_no')
        stu = Student.objects.filter(stu_no=stu_no).first()
        return render(request, 'student/center.html', locals())

    def post(self, request):
        change = ChangePassword(request.POST)
        if change.is_valid():
            stu_no = request.session.get('login_no')
            stu = Student.objects.filter(stu_no=stu_no).first()
            stu.password = request.POST['password']
            stu.save()
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': change.errors['password']})


class Email(View):
    def get(self, request):
        stu_no = request.GET['stu_no']
        email = request.GET['email']
        stu = Student.objects.filter(stu_no=stu_no).first()
        stu.email = email
        stu.save()
        return redirect('/student/center')

    def post(self, request):
        # 验证邮箱格式
        import re
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', request.POST['email']):
            # 拿到用户原邮箱
            stu_no = request.session.get('login_no')
            student_info = Student.objects.filter(stu_no=stu_no).first()
            old_email = student_info.email
            # 如果原来有邮箱
            if old_email:
                # 发送链接至原邮箱
                host = request.get_host()
                send_title = WEBNAME
                url = 'http://' + host + '/student/email/?stu_no=' + stu_no + '&email=' + request.POST['email']
                send_body = '请点击确认邮箱'
                body = '<a href="{}">确定</a>'.format(url)
                try:
                    send_mail(send_title, send_body, EMAIL_FROM, [old_email], html_message=body)
                    return JsonResponse({'status': 'ok', 'msg': '请前往邮箱{}进行修改'.format(old_email)})
                except:
                    return JsonResponse({'status': 'fail', 'msg': '邮件发送失败，请重新尝试'})
            else:
                student_info.email = request.POST['email']
                student_info.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱格式不正确'})


def exam(request, exam_id):
    paper = Exam.objects.filter(pk=exam_id).first().paper_no
    stu_no = request.session.get('login_no')
    # 试卷试题
    exam = CreatePaper.objects.filter(paper_no=paper).all()
    questions = []

    # 考试学生信息
    stu_info = Student.objects.filter(stu_no=stu_no).first()
    # 试卷信息
    paper_info = Paper.objects.filter(paper_no=paper.paper_no).first()
    for e in exam:
        questions.append(e.question_no)
    return render(request, 'student/exam.html', {
        'questions': questions,
        'stu_info': stu_info,
        'paper_info': paper_info
    })


def check_answer(request):
    answer_list = request.POST.getlist('answer')
    stu_no = request.session.get('login_no')
    paper_no = request.POST['paper_no']

    questions = CreatePaper.objects.filter(paper_no__paper_no=paper_no).all()
    # 获取标准答案及其分值
    q_answer_list = {}
    total_grade = 0
    for i, q in enumerate(questions):
        q_answer_list[i] = (q.question_no.answer, q.question_no.score)
        total_grade += q.question_no.score

    # 计算得分
    grade = 0
    for i in range(len(answer_list)):
        if answer_list[i] == q_answer_list[i][0]:
            grade += q_answer_list[i][1]
    grade = round((grade * 100) / total_grade, 1)
    # 找到学生考试的试卷将考试信息改为已考并记录成绩
    exam = Exam.objects.filter(Q(paper_no__paper_no=paper_no) & Q(stu_no__stu_no=stu_no)).first()
    exam.is_finish = True
    exam.grade = grade
    exam.save()

    return JsonResponse({'status': 'ok', 'msg': 'error'})
