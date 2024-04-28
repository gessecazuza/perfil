###################################################################
###### Modelo para as Questões do Quiz em questão #################
###################################################################

from django.db import models
from django.db.models import Sum
from quizes.models import Quiz

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, help_text="Título - 200 caracteres")
    created = models.DateTimeField(auto_now_add=True)
    points = models.FloatField(default=0, help_text="Valor da questão")

    def __str__(self):
        return f"{self.quiz}, Pergunta: {self.text}"

    #Obtém todas as alternativas (answers) das questions num subSet pela chave estrangeira (pk)
    def get_answers(self):
        return self.answer_set.all().order_by('question_id','text')

    class Meta:
        verbose_name_plural = 'Questões'

''' Classe para as alternativas. Isto dispensaria um terceiro app (answers) 
    que trataria apenas das alternativas possíveis 
'''
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=120, help_text="Alternativa - 120 caracteres")
    correct = models.BooleanField(default=False, help_text="Resposta certa?")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question.text}, Alternativa: {self.text}"

    class Meta:
        verbose_name_plural = 'Alternativas'