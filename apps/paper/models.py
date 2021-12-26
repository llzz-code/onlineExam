from django.db import models
from student.models import Student

# Create your models here.
from teacher.models import Teacher

ANSWER = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)
LEVEL = {
    ('1', '简单'),
    ('2', '一般'),
    ('3', '困难'),
}
DURATION = {
    ('1', '150分钟'),
    ('2', '100分钟'),
    ('3', '90分钟'),
    ('4', '60分钟')
}
class Subject(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=30, verbose_name='科目')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '科目'

class QuestionBank(models.Model):
    # id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name='所属科目', on_delete=models.CASCADE)
    title = models.TextField(verbose_name='题目')
    option_a = models.CharField(verbose_name='A', max_length=100)
    option_b = models.CharField(verbose_name='B', max_length=100)
    option_c = models.CharField(verbose_name='C', max_length=100)
    option_d = models.CharField(verbose_name='D', max_length=100)
    answer = models.CharField(verbose_name='答案', choices=ANSWER, max_length=4)
    level = models.CharField(verbose_name='难度', choices=LEVEL, max_length=10)
    score = models.IntegerField(verbose_name='分数', default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = '试题管理'


class Paper(models.Model):
    paper_no = models.CharField(max_length=20, verbose_name='试卷编号')
    title = models.CharField(max_length=50, verbose_name='试卷', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='出题教师', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='所属科目', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='考试时间')
    duration = models.CharField(verbose_name='考试时长', choices=DURATION, max_length=50)

    def __str__(self):
        return '[' + self.paper_no + ']' + self.title if self.title else ''

    class Meta:
        verbose_name_plural = verbose_name = '试卷'


class CreatePaper(models.Model):
    paper_no = models.ForeignKey(Paper, verbose_name='所属试卷', on_delete=models.CASCADE)
    question_no = models.ForeignKey(QuestionBank, verbose_name='试题', on_delete=models.CASCADE)

    def __str__(self):
        return self.paper_no

    class Meta:
        verbose_name_plural = verbose_name = '组卷'


class Exam(models.Model):
    stu_no = models.ForeignKey(Student, verbose_name='考试学生', on_delete=models.CASCADE)
    paper_no = models.ForeignKey(Paper, verbose_name='考试试卷', on_delete=models.CASCADE)
    is_finish = models.BooleanField(verbose_name='是否完成', default=False)
    grade = models.FloatField(verbose_name='成绩', default=0)

    def __str__(self):
        return self.paper_no.title

    class Meta:
        verbose_name_plural = verbose_name = '学生考试'


