from django.contrib import admin
from paper.models import QuestionBank, Paper, CreatePaper


# Register your models here.

class QuestionBankAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'subject', 'title', 'option_a',
        'option_b', 'option_c', 'option_d',
        'answer', 'level', 'score'
    ]


class PaperAdmin(admin.ModelAdmin):
    list_display = ['paper_no', 'teacher',
                    'subject', 'time', 'duration'
                    ]


class CreatePaperAdmin(admin.ModelAdmin):
    list_display = [
        'paper_no', 'question_no'
    ]


admin.site.register(QuestionBank, QuestionBankAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(CreatePaper, CreatePaperAdmin)