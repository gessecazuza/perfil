from django.db import models
from quizes.models import Quiz
from personality.models import Personalidade

#Para capturar o usuário que respondeu o quiz
from django.conf import settings
from django.contrib.auth.models import User


###################################################################
###### Modelo para os resultados - Relatórios  #################
###################################################################

#Classe para os resultados finais dos quiz
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    #personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(help_text="Data do teste", verbose_name="Criado em:")
    scorePerfil = models.FloatField(help_text="Perfil Traçado", verbose_name="Perfil Determinante (%):")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    personalidade = models.IntegerField()
    nameProfile = models.CharField(max_length=30, default="", verbose_name="Nome do Perfil:")
    score = models.FloatField(default=1, verbose_name="Aprovação Exigida (%):")
    totalAnswered = models.FloatField(default=1, verbose_name="Total respondido (%):")
    duration = models.FloatField(default=1)
    scoreDominante = models.FloatField(default=1, help_text="Nota Perfil Dominante")
    scoreInfluente = models.FloatField(default=1, help_text="Nota Perfil Influente")
    scoreEstavel = models.FloatField(default=1, help_text="Nota Perfil Estável")
    scoreCauteloso = models.FloatField(default=1, help_text="Nota Perfil Cauteloso")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Resultados'
    
    #O método set_calcula_perfil não precisa ser um método de instância, 
    # pois não usa nenhum atributo específico da instância Result. Será estático.
    @staticmethod
    def set_calcula_perfil(listPerfil):
        return max(listPerfil)