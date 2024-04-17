from django.db import models
from questions.models import Answer

##### Classe para os tipos de perfis 
##### [01 - Dominancia]; [02 - Influencia]; [03 - Estabilidade]; [04 - Cautela]
class Personalidade(models.Model):
    TIPO_PERFIL_CHOICES = (
        (1, ('1. DOMINANTE')),
        (2, ('2. INFLUENTE')),
        (3, ('3. ESTAVEL')),
        (4, ('4. CAUTELOSO')),
        
    )
    NOME_PERFIL_CHOICES = (
        ('D',('DOMINANCIA')),
        ('DI',('DOMINANCIA-INFLUÊNCIA')),
        ('DC',('DOMINANCIA-CAUTELA')),
        ('I',('INFLUENCIA')),
        ('ID',('INFLUENCIA-DOMINÂNCIA')),
        ('IE',('INFLUENCIA-ESTAVEL')),
        ('ESTAVEL',('ESTABILIDADE')),
        ('CAUTELOSO',('CAUTELA')),
    )
    personalidade = models.IntegerField(choices=TIPO_PERFIL_CHOICES, default=0)
    name = models.CharField(max_length=30, choices=NOME_PERFIL_CHOICES, default="")
    describe = models.CharField(max_length=256, help_text="Resumo sobre o perfil - 256 caracteres")

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['personalidade']
        verbose_name_plural = 'Personalidades'

    #Obtém todas as características de cada perfil
    def get_definicoes(self):
        return self.definicao_set.all()

    # Obtém todas as profissões de cada perfil
    def get_profissao(self):
        return self.profissao_set.all()
    
    #obtem os Motivadoresde Carreira
    #Deve ser em minúsculo para gerar querySet
    def get_motivadorescarreira(self):
        return self.motivadorescarreira_set.all()
    
    #obtem uma lista do quadro compartivo entre os 04 perfis
    #Deve ser em minúsculo para gerar querySet
    def get_quadroscomparativos(self):
        return self.quadrocomparativo_set.all()
        
    # Índice de Pontos de Melhoria - IPM ipmDisc
    def get_ipmdisc(self):
        return self.ipmdisc_set.all()

####### Classe com as definições detalhadas de cada Tipo de perfil
class Definicao(models.Model):
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE)
    concept = models.TextField(max_length=1512, default="", help_text="Definição geral")
    strikingTraits = models.CharField(max_length=1024, default="", help_text="Traços marcantes")
    characteristics = models.CharField(max_length=1024, default="", help_text="Características marcantes")
    positives = models.CharField(max_length=756, help_text="Pontos positivos")
    negativeTraits =  models.CharField(max_length=1024, default="", help_text="Traços negativos")
    limitingPoints = models.CharField(max_length=1024, default="", help_text="Pontos limitantes")
    improvementPoints = models.CharField(max_length=1024, default="", help_text="Pontos a serem melhorados")
    NeedsFears = models.CharField(max_length=1024, default="", help_text="Necessidades e medos")
    motivatingFactors = models.CharField(max_length=1024, default="", help_text="Fatores motivadores")
    teamValue = models.CharField(max_length=1024, default="", help_text="Valor na Equipe")
    idealEnvironment = models.CharField(max_length=1024, default="", help_text="Ambiente Ideal")
    coexistence = models.CharField(max_length=1024, default="", help_text="Convivendo com ele... como agir?")
    withChallenges =  models.CharField(max_length=1024, default="", help_text="Como agem com novos desafios?")
    howTheyLead = models.CharField(max_length=1024, default="", help_text="Como costumam liderar?")
    decisionMakin = models.CharField(max_length=1024, default="", help_text="Como tendem a tomar decisão?")
    underPressure = models.CharField(max_length=1024, default="", help_text="Sob Pressão")
    combinations = models.TextField(max_length=1512, default="", help_text="Possíveis Combinações")

    def __str__(self):
        return str(self.personalidade)

    class Meta:
        verbose_name_plural = 'Definição do Perfil'

###### Classe com as profissões para cada tipo de Perfil
class Profissao(models.Model):
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE)
    actingArea = models.CharField(max_length=1024, default="", help_text="Área de Atuação")
    profession = models.CharField(max_length=512, default="", help_text="Nome da Profissão")
    description = models.CharField(max_length=1024, default="", help_text="Descrição da Função")
    
    class Meta:
        ordering = ['personalidade']
        verbose_name_plural = 'Profissões'

    def __str__(self):
        #return str({self.personalidade}, {self.actingArea})
        return str(f"{self.actingArea}, {self.personalidade}")
    
##### Classe dos itens MOTIVADORES DE CARREIRA - Teste DISC
class MotivadoresCarreira(models.Model):
    #personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE)
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=1024, default="")
    howToAct = models.CharField(max_length=1024, help_text="Como o influenciar?")
    
    class Meta:
        verbose_name_plural = 'Motivadores'
    
    def __str__(self):
        return str(self.personalidade)

####### Quadro Comparativo entre os perfis - Alta e baixa dimensao
class QuadroComparativo(models.Model):
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE)
    highDimension = models.CharField(max_length=100, default="", help_text="Alta dimensão")
    lowDimension = models.CharField(max_length=100, default="", help_text="Baixa dimensão")
    mainFeatures = models.CharField(max_length=100, default="", help_text="Características principais")
    
    class Meta:
        verbose_name_plural = "Quadro Comparativo"
    
    def __str__(self):
        return str(self.personalidade)
    
###### Índice de Pontos de Melhoria - IPM - Apostila Disc - Pag 68
class ipmDisc(models.Model):
    TIPO_IPM_CHOICES = (
        ("1", ('1. NULO')),
        ("2", ('2. MUITO BAIXO')),
        ("3", ('3. BAIXO')),
        ("4", ('4. NORMAL BAIXO')),
        ("5",('5. NORMAL')),
        ("6",('6. NORMAL ALTO'))
    )
    personalidade = (models.ForeignKey(Personalidade, on_delete=models.CASCADE))
    name = models.CharField(max_length=100, default="", help_text="Nome do ponto negativo reconhecido")
    description = models.CharField(max_length=512, default="", help_text="Descrição do ponto negativo")
    indice = models.DecimalField(max_digits=5, decimal_places=2, help_text="Soma de pontos negativos")
    tipo_indice = models.CharField(max_length=20, choices=TIPO_IPM_CHOICES, default="1")

    class Meta:
        verbose_name_plural = "Indice de Pontos de Melhora(IPM)"

    def __str__(self):
        return str(self.personalidade)