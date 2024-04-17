from django.contrib import admin

# Register your models here.
from .models import Question, Answer

#### Para as Perguntas terá um tab-line que permite juntar na mesma 
# janela Questions e Answers

class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)