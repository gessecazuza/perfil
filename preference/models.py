from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#Para o campo duração do cookie como data até 07 dias
from  django.utils import timezone
from datetime import timedelta

# Create your models here.
class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    dataAdesao = models.DateTimeField(auto_now_add=True)
    SO = models.CharField(max_length=50, default="Windows")
    VersaoSO = models.CharField(max_length=50, default="")
    arquitetura = models.CharField(max_length=50, default="")
    processador = models.CharField(max_length=50, default="")
    navegador = models.CharField(max_length=70, default="")
    ipTerminal = models.CharField(max_length=30, default="")
    pais = models.CharField(max_length=70, default="")
    cidade = models.CharField(max_length=70, default="")
    idioma = models.CharField(max_length=50, default="")
    aceitouTermos = models.BooleanField(default=True)
    analyticsCookies = models.BooleanField(default=False)
    marketingCookies = models.BooleanField(default=False)
    
    def __str__(self):
        #return f"{self.user}"
        return str(self.user)
    
    def get_cookies(self):
        return self.cookies_set.all()
    
    class Meta:
        verbose_name_plural = 'Preferências'
    
class Cookies(models.Model):
    TIPO_COOKIE_CHOICES = (
        ('0. RECUSADO', ('RECUSADO')),
        ('1. OBRIGATORIO', ('OBRIGATORIO')),
        ('2. PREFERENCIAS', ('PREFERENCIAS')),
        ('3. ESTATICOS', ('ESTATISTICOS')),
        ('4. MARKETING', ('MARKETING')),
    )
    DESCRICAO_CHOICES = (
        ('RECUSADO', ('Cliente recusou os termos de gravação.')),
        ('OBRIGATORIO', ('Cookies necessários para geração do teste DISC.')),
        ('PREFERENCIAS', ('Cliente pode definir os que deseja gravar.')),
        ('ESTATICOS', ('Permite colher dados de uso, tempo, e conteúdo da navegação.')),
        ('MARKETING', ('Permite campanhas de marketing para melhorar relacionamento e ofertas.')),
    )
    preferencia = models.ForeignKey(Preference, on_delete=models.CASCADE)
    tipoCookie = models.CharField(max_length=30, choices=TIPO_COOKIE_CHOICES, default='OBRIGATORIO')
    descricao = models.CharField(max_length=256, choices=DESCRICAO_CHOICES, default="")
    durationCookie = models.DateTimeField(null=True, default=timezone.now() + timedelta(days=7))
  
    def __str__(self):
        return str(self.preferencia)
      
    class Meta:
        verbose_name_plural = 'Cookies'