from django.db import models
import random
from random import sample

#Para capturar o usuário criador do quiz
from django.conf import settings
from django.contrib.auth.models import User

DIFF_CHOICES = (
    ('Fácil', 'Fácil'),
    ('Médio', 'Médio'),
    ('Avançado', 'Avançado'),
)
""" ###### APÓS UMA RESTAURAÇÃO DE BD PostgresSQL, pode ser necessário redefinir as PK com sequência de incremento automático (ID) ####

1. Tabela quizes_quiz
SELECT setval('quizes_quiz_id_seq', (SELECT MAX(id) FROM quizes_quiz)+1);

2.Tabela questions_question
SELECT setval('questions_question_id_seq', (SELECT MAX(id) FROM questions_question)+1);

3. Tabela questions_answer
SELECT setval('questions_answer_id_seq', (SELECT MAX(id) FROM questions_answer)+1);

"""
class Quiz(models.Model):

    name = models.CharField(max_length=100, verbose_name="Nome geral:")
    topic = models.CharField(max_length=100, verbose_name="Tema específico:")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Criado em:")
    number_of_questions = models.IntegerField(verbose_name="Questões:", help_text="Número de questões")
    time = models.IntegerField(verbose_name="Tempo:", help_text="Tempo máximo em minutos")
    required_score_to_pass = models.IntegerField(verbose_name="Pontuação", help_text="Pontuação exigida para aprovação em %")
    difficulty = models.CharField(max_length=10, choices=DIFF_CHOICES, verbose_name="Nível:")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    #Método que retorna a definção de String do Objeto (nome e tópico)
    def __str__(self):
        #return f"{self.name}-{self.topic}"
        return f"{self.name}"

    #Método que obtém todas as questions (questões) ligadas pela chave estrangeria
    def get_questions(self):
       
       # Obtém o número de perguntas limitadas ao total definida de number_of_questions
       ''' 
       questions = list(self.question_set.all())
       random.shuffle(questions)  #Pega aletoriamente uma pergunta
       return questions[:self.number_of_questions]
       '''
       questions = list(self.question_set.all())
       num_questions = min(self.number_of_questions, len(questions))
       random_questions = sample(questions, num_questions)
       return random_questions

    class Meta:
        verbose_name_plural = 'Questionários'
        

