#import uuid 				#Gera nomes aleatórios
from accounts.models import Perfil
from django.contrib.auth.models import User
from django.test import TestCase  # módulo padrão python de testes
from model_mommy import mommy  # módulo para automação de objetos
from personality.models import (Definicao, MotivadoresCarreira, Personalidade,
                                Profissao, QuadroComparativo, ipmDisc)
from preference.models import Preference
from questions.models import Question
from quizes.models import Quiz
from random import shuffle

from result.models import Result

###########################################################################
####### MODEL ACCOUNTS  - Método STR  #####################################
###########################################################################
class test_PerfilTestCase(TestCase):
    def setUp(self):
        self.perfil = mommy.make('Perfil')
    
    def test_str(self):
        self.assertEquals(str(self.perfil), str(self.perfil.usuario))

###########################################################################
####### MODEL PERSONALITY  - Método STR e query_set.all() #################
###########################################################################
class PersonalidadeTestCase(TestCase): #Herdará de TestCase

    #Construtor central
    def setUp(self):
        #Gera um objeto local (self.personalidade) da classe Personalidade para comparação
        self.personalidade = mommy.make("Personalidade") #Para o teste STR individual
        self.personalidades = mommy.make("Personalidade", _quantity=4) #Para a Query definicao_set.all()
    

    #Método que fará o teste individual do STR
    def test_str(self):
        #Os dois são iguais, ou seja, o que o mommy.make gerou com o retorno do método str?
        self.assertEquals(str(self.personalidade), self.personalidade.name)

    ###################################################################################
    #### Testa o query_set.all() das definicoes, profissoes, motivadoresCarreira,
    #### QuadroComparativo e IpmDisc - Geram 04 instâncias para comparação
    ###################################################################################
    def test_get_definicoes(self):
        for personalidade in self.personalidades:
            definicoes = personalidade.get_definicoes()
            self.assertEqual(definicoes.count(), 0)  # Verifica se não há definicoes inicialmente

            # Crie algumas definicoes usando a biblioteca mommy associadas à personalidade atual
            mommy.make('Definicao', _quantity=3, personalidade=personalidade)

            #Gera uma lista (query) de várias definições por personalidade
            definicoes = personalidade.get_definicoes()
            
            # Verifica se existem 3 definicoes associadas à personalidade atual
            self.assertEqual(definicoes.count(), 3) 

    def test_get_profissao(self):
        for personalidade in self.personalidades:
            profissoes = personalidade.get_profissao()
            self.assertEqual(profissoes.count(), 0)
            mommy.make('Profissao', _quantity=3, personalidade=personalidade)
            profissoes = personalidade.get_profissao()
            self.assertEqual(profissoes.count(), 3)

    def test_get_motivadorescarreira(self):
        for personalidade in self.personalidades:
            motivadores = personalidade.get_motivadorescarreira()
            self.assertEqual(motivadores.count(), 0)
            mommy.make('MotivadoresCarreira', _quantity=3, personalidade=personalidade)
            motivadores = personalidade.get_motivadorescarreira()
            self.assertEqual(motivadores.count(), 3)

    def test_get_quadroscomparativos(self):
        for personalidade in self.personalidades:
            quadros = personalidade.get_quadroscomparativos()
            self.assertEqual(quadros.count(), 0)
            mommy.make('QuadroComparativo', _quantity=3, personalidade=personalidade)
            quadros = personalidade.get_quadroscomparativos()
            self.assertEqual(quadros.count(), 3)        

    def test_get_ipmdisc(self):
        for personalidade in self.personalidades:
            ipms = personalidade.get_ipmdisc()
            self.assertEqual(ipms.count(), 0)
            mommy.make('ipmDisc', _quantity=3, personalidade=personalidade)
            ipms = personalidade.get_ipmdisc()
            self.assertEqual(ipms.count(), 3)  

   
###############################################################################
####### MODEL PERSONALITY - Classe Definicao - Método STR ###################
###############################################################################
class DefinicaoTestCase(TestCase):
    def setUp(self):
        self.definicao = mommy.make('Definicao')

    def test_str(self):
        # Converter os 02 objetos para Str e evitar o erro: AssertionError ou 
        # asserção falhou (declaração de verificação)  
        self.assertEquals(str(self.definicao), str(self.definicao.personalidade))    


#########################################################
####### Classe PROFISSAO - Método STR ###################
#########################################################
class ProfissaoTestCase(TestCase):
    def setUp(self):
        self.profissao = mommy.make('Profissao')

    def test_str(self):
        self.assertEquals(str(self.profissao), str(f"{self.profissao.actingArea}, {self.profissao.personalidade}"))  

#########################################################
####### Classe MotivadoresCarreira - Método STR ###################
#########################################################
class MotivadoresCarreiraTestCase(TestCase):
    def setUp(self):
        self.motivadoresCarreira = mommy.make('MotivadoresCarreira')

    def test_str(self):
        self.assertEquals(str(self.motivadoresCarreira), str(self.motivadoresCarreira.personalidade)) 


#########################################################
####### Classe ipmDisc - Método STR ###################
#########################################################
class ipmDiscTestCase(TestCase):
    def setUp(self):
        self.ipmdisc = mommy.make('ipmDisc')

    def test_str(self): 
        self.assertEquals(str(self.ipmdisc), str(self.ipmdisc.personalidade)) 

#########################################################
####### Classe QuadroComparativo - Método STR ###########
#########################################################
class QuadroComparativoTestCase(TestCase):
    def setUp(self):
        self.quadroComparativo = mommy.make('QuadroComparativo')

    def test_str(self):
        self.assertEquals(str(self.quadroComparativo), str(self.quadroComparativo.personalidade)) 


###########################################################################
####### MODEL PREFERENCE  - Método STR e query_set.all() ###############
###########################################################################
class PreferenceTestCase(TestCase):
    def setUp(self):
        self.preference = mommy.make("Preference")
        self.preferencias = mommy.make('Preference', _quantity=2)

    def test_str(self):
        self.assertEquals(str(self.preference), str(self.preference.user))

    #Método querySet: cookies_set.all()
    def test_get_cookies(self):
        for p in self.preferencias:
            cookies = p.get_cookies()
            self.assertEqual(cookies.count(), 0)
            mommy.make('Cookies', _quantity=2, preferencia=p)
            cookies = p.get_cookies()
            self.assertEqual(cookies.count(), 2)  

#########################################################
####### Classe Preference.Cookies - Método STR ###################
#########################################################
class CookiesTestCase(TestCase):
    def setUp(self):
        self.cookie = mommy.make("Cookies")

    def test_str(self):
        self.assertEquals(str(self.cookie), str(self.cookie.preferencia))


###########################################################################
####### MODEL QUIZ  - Método STR e query_set.all() ###############
###########################################################################
class QuizTestCase(TestCase):
    # Cria manualmente um objeto User
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword') 
        self.quiz = mommy.make(
            Quiz,
            name='Quiz Test',
            topic='Test Topic',
            number_of_questions=5,
            time=10,
            required_score_to_pass=70,
            difficulty='Easy',
            user=self.user,  # Atribui o objeto User criado manualmente
        )

    def test_get_questions(self):
        # Cria perguntas de teste relacionadas ao Quiz
        # O _ dispensa uso de uma variável, indicando que o valor não é 
        # relevante para a execução do loop.
        for _ in range(10):
            mommy.make('Question', quiz=self.quiz)

        # Verifica se o número de perguntas retornadas pelo método get_questions
        # corresponde ao número definido no campo number_of_questions do Quiz.
        questions = self.quiz.get_questions()
        self.assertEqual(len(questions), self.quiz.number_of_questions)

        # Verifica se as perguntas retornadas estão realmente relacionadas ao Quiz.
        for questao in questions:
            self.assertEqual(questao.quiz, self.quiz)


###########################################################################
####### MODEL QUESTIONS  - Método STR e query_set.all() ###############
###########################################################################
class QuestionsTestCase(TestCase):
    def setUp(self):
        self.question = mommy.make('Question')
        self.questions = mommy.make('Question', _quantity=4)
    
    def test_str(self):
        self.assertEqual(str(self.question), str(f"{self.question.quiz}, Pergunta: {self.question.text}")) 

    def test_get_answers(self):
        for a in self.questions:
            respostas = a.get_answers()
            self.assertEqual(respostas.count(), 0)
            mommy.make('Answer', _quantity=3, question=a)
            respostas = a.get_answers()
            self.assertEqual(respostas.count(), 3)


######### MODEL QUESTION.ANSWER  - STR ##########################
class AnswerTestCase(TestCase):
    def setUp(self):
        self.answer = mommy.make('Answer')
    
    def test_str(self):
        self.assertEqual(str(self.answer), str(f"{self.answer.question.text}, Alternativa: {self.answer.text}"))


###########################################################################
####### MODEL RESULT  - Método STR e set_calcula_perfil(listPerfil) #######
###########################################################################
class ResultTestCase(TestCase):
    def setUp(self):
        self.resultado = mommy.make('Result')

    #Testa o STR
    def test_str(self):
        self.assertEqual(str(self.resultado), str(self.resultado.user))

    #Testa o set_calcula_perfil(listPerfil)
    def test_set_calcula_perfil(self):
        lista_de_perfis = [10, 20, 15, 30, 25]  #Lista de perfis fictícia para o teste
        perfil_maximo = Result.set_calcula_perfil(lista_de_perfis) # Passando a lista de perfis
        self.assertEqual(perfil_maximo, max(lista_de_perfis))      # Verifica se o valor retornado é o máximo da lista