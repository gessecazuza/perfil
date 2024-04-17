from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from model_mommy import mommy
from django.contrib.auth.models import Group, User
from django.http import Http404
from urllib.parse import quote

from accounts.views import UsuarioCreate, PerfilUpdate
from accounts.models import Perfil
from preference.models import Preference

###Para testar o model Quiz, Question e Answer
from django.core.paginator import Paginator
from quizes.models import Quiz
from questions.models import Question, Answer

from result.models import Result, Personalidade
from result.views import render, Pdf_Disc
from quizes.views import ListaQuizes, disc_questions, save_quiz_view, atualiza_perfil

#Captuar o token na requisição via form
from django.middleware import csrf

### Para testar o envio de E-mail
from quizes.forms import ContatoForm

#########################################################################################
####### 1. ACCOUNTS - VIEWS UsuarioCreate - Método def form_valid(self, form) ###########
#########################################################################################
class UsuarioCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('novo-usuario')

    #### Testa a gravação de novo User - accounts\template\form.html
    def test_usuario_create_success(self):
        # Defina os dados do usuário que você deseja usar para o teste
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # Envie uma requisição POST para a view de registro com os dados do usuário
        response = self.client.post(self.url, user_data)

        # Verifique se o usuário foi criado com sucesso (código de status 302 para redirecionamento)
        self.assertEqual(response.status_code, 302)

        # Verifique se o usuário está no banco de dados
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verifique se um perfil foi criado para o usuário
        user = User.objects.get(username='testuser')
        self.assertTrue(Perfil.objects.filter(usuario=user).exists())

    #### Testa os parâmetros enviados ao template accounts\template\form.html
    def test_get_context_data(self):
        # Envie uma requisição GET para a view de registro
        response = self.client.get(self.url)

        # Verifique se a view retorna o código de status 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifique se o contexto contém as chaves 'titulo' e 'botao'
        self.assertIn('titulo', response.context)
        self.assertIn('botao', response.context)

        # Verifique se os valores das chaves 'titulo' e 'botao' são os esperados
        self.assertEqual(response.context['titulo'], "REGISTRO DE NOVO USUÁRIO")
        self.assertEqual(response.context['botao'], "CADASTRAR")


#########################################################################################
####### 1.1 - ACCOUNTS - VIEWS PerfilUpdate - Método def form_valid(self, form) ###########
#########################################################################################
class PerfilUpdateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuarioteste",
            password="senhateste",
        )
        self.perfil = mommy.make(Perfil, usuario=self.user)

    def test_get_object_existente(self):
        self.client.login(username="usuarioteste", password="senhateste")

        url = reverse("atualizar-dados") 
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["perfil"], self.perfil)

    
    def test_get_context_data(self):
        self.client.force_login(self.user)  # Autentica o usuário para o teste

        url = reverse("atualizar-dados") 
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
      
        self.assertEqual(response.context["titulo"], "ATUALIZAÇÃO CADASTRAL")
        self.assertEqual(response.context["botao"], "CONFIRMAR")

#########################################################################################
####### 2. PERSONALITY - VIEWS - SEM MÓDULOS  ###########################################
#########################################################################################

#########################################################################################
####### 3. PREFERENCE - VIEWS - def politicaPrivacidade(request):########################
#########################################################################################
class PreferenceViewTestCase(TestCase):
    def setUp(self):
        # Criar um usuário autenticado para usar nos testes
        self.user = mommy.make(User)
        self.user.set_password('testpassword')
        self.user.save()

        # Logar o usuário
        self.client.login(username=self.user.username, password='testpassword')

        # URL da view aceitar_cookies
        self.url = reverse('preference:aceitar_cookies')

        # Criar uma instância de Preference para o usuário
        self.preference = mommy.make(Preference, user=self.user, aceitouTermos=True)
        self.preference.save()

        # URL da view localizaUsuario
        self.urlLocaliza = reverse('preference:localizacao')

    ''' 
    3.1 - Simula uma solicitação POST com dados válidos para aceitar os cookies. 
    Ele verifica se a resposta HTTP é bem-sucedida (código 200), se o template 
    correto está sendo renderizado, se a preferência foi criada corretamente no 
    banco de dados e se os valores salvos na preferência estão corretos.
    ''' 
    def test_aceitar_cookies(self):
        # Simular a solicitação POST usando model_mommy para criar os dados
        data = {
            'analytics_cookies': False,
            'marketing_cookies': False,
        }

        # Simular a solicitação POST
        response = self.client.post(self.url, data)

        # Restaurar as preferências do usuário
        self.user.refresh_from_db()

        # Verificar se a resposta HTTP é bem-sucedida (código 200)
        self.assertEqual(response.status_code, 200)

        # Verificar se o template correto está sendo renderizado
        self.assertTemplateUsed(response, 'index.html')

        # Verificar se a preferência foi criada no banco de dados
        preference = Preference.objects.filter(user=self.user)
        self.assertTrue(preference.exists())

        # Verificar os valores salvos na preferência
        preference = preference.first()
        self.assertEqual(preference.user, self.user)
        self.assertTrue(preference.aceitouTermos)
        self.assertFalse(preference.analyticsCookies)
        self.assertFalse(preference.marketingCookies)
    

    ''' 3.2 - Recebe uma requisição simples, via URl e devolve ao template politica.html '''
    def test_politica_privacidade(self):
        # Use a função reverse para obter a URL com base no nome da view
        url = reverse('preference:politica')

        # Faça uma solicitação GET à URL da view
        response = self.client.get(url)

        # Verifique se a resposta HTTP é bem-sucedida (código 200)
        self.assertEqual(response.status_code, 200)

#########################################################################################
####### 3.3 QUIZES - VIEWS -                                        #####################
#########################################################################################
class LocalizaUsuarioViewTestCase(TestCase):

    def setUp(self):
        # Criar um cliente de teste para fazer as requisições
        self.client = Client()

        # Criar um usuário para fins de teste
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Criar um objeto Preference associado ao usuário
        self.preference = mommy.make('preference.Preference', user=self.user, 
            ipTerminal = '127.0.0.1',
            aceitouTermos=True, analyticsCookies = True, marketingCookies = True, 
            navegador = 'Crome', SO = 'Windows 8', VersaoSO = '8.1 Pro', 
            arquitetura ='64bit', processador = 'AMD Core Phanthon',
            idioma ='PORT-BRA', pais = 'Desconhecido', cidade = 'Não localizada'
        )

        # Definir a URL para testar a view
        self.url = reverse('preference:localizacao')
    
    ### 3.4 - Pesquisa o usuário logado, busca as preferências em BD e devolve ao 
    # template localizacao.html
    def test_localiza_usuario(self):

        # Simular o acesso real à view
        self.client.force_login(self.user)

        # Fazer uma requisição GET para a URL da view
        response = self.client.get(self.url)

        # Verificar se o código de status da resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar se a resposta contém os dados esperados do objeto Preference no contexto
        self.assertContains(response, self.user.username)
        self.assertContains(response, str(self.preference.aceitouTermos).lower())
        self.assertContains(response, str(self.preference.marketingCookies).lower())
        self.assertContains(response, str(self.preference.analyticsCookies).lower())

        # Verificar se o endereço ipTerminal está no contexto da resposta
        self.assertEqual(response.context['dados']['ipTerminal'], self.preference.ipTerminal)

        # Verificar outros dados importantes no contexto da resposta
        self.assertEqual(response.context['dados']['SO'], self.preference.SO)
        self.assertEqual(response.context['dados']['VersaoOS'], self.preference.VersaoSO)
        self.assertEqual(response.context['dados']['arquitetura'], self.preference.arquitetura)
        self.assertEqual(response.context['dados']['processador'], self.preference.processador.split(',')[0])
        self.assertEqual(response.context['dados']['idioma'], self.preference.idioma.split(',')[0])
        self.assertEqual(response.context['dados']['aceitouTermos'], self.preference.aceitouTermos)
        self.assertEqual(response.context['dados']['marketing'], self.preference.marketingCookies)
        self.assertEqual(response.context['dados']['analiticos'], self.preference.analyticsCookies)
        self.assertEqual(response.context['dados']['pais'], self.preference.pais)
        self.assertEqual(response.context['dados']['cidade'], self.preference.cidade)

    #### 3.5 - Testa a requisição sem LOGIN e redireciona ao login
    def test_localiza_usuario_nao_autenticado(self):
        # Fazer uma requisição GET para a URL da view sem autenticar o usuário
        response = self.client.get(self.url)

        # Verificar se o código de status da resposta é 302 (redirecionamento para a página de login)
        self.assertEqual(response.status_code, 302)

        # Verificar se o redirecionamento leva o usuário para a página de login
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

#########################################################################################
######################## 4 - QUIZES - VIEWS -                           #################
#########################################################################################

#Testa a requisição via browser, tanto logado como não logado 
class IndexViewTestCase(TestCase):

    def setUp(self):

        # Construtor que Cria um usuário para simular login
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        # URLS para as páginas: Index / Sobre / Servico / TesteDisc
        self.url_index = reverse('quizes:index')
        self.url_sobre = reverse('quizes:sobre')
        self.url_servico = reverse('quizes:servico')
        self.url_teste_disc = reverse('quizes:teste-disc')

    # 4.1 - testa se está locado - O retorno será um código 200 (sucesso)
    def test_index_view_logado(self):
        
        # Faz uma requisição GET para a página inicial
        response = self.client.get(self.url_index)
        # Verifica se o código de status da resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Verifica se o template correto está sendo usado
        self.assertTemplateUsed(response, 'index.html')

    # 4.2 - Se NÃO está logado - O retorno será um código 302 (erro e redireciona)
    def test_index_view_nao_logado(self):
        # Faz logout do usuário criado no setUp
        self.client.logout()
        # Faz uma requisição GET para a página inicial
        response = self.client.get(self.url_index)
        # Verifica se o código de status da resposta é 302 (redirecionamento para a página de login)
        self.assertEqual(response.status_code, 302)
        # Verifica se o redirecionamento para a página de login está correto
        self.assertRedirects(response, f'/accounts/login/?next={self.url_index}')

    # 4.3 - testa se está locado - O retorno será um código 200 (sucesso)
    def test_sobre_view_logado(self):
        response = self.client.get(self.url_sobre)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sobre.html')

    # 4.4 - Se NÃO está logado - O retorno será um código 302 (erro e redireciona)
    def test_sobre_view_nao_logado(self):
        self.client.logout()
        response = self.client.get(self.url_sobre)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.url_sobre}')
    
    # 4.4 - testa se está locado - O retorno será um código 200 (sucesso)
    def test_servico_view_logado(self):
        response = self.client.get(self.url_servico)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')

    # 4.5 - Se NÃO está logado - O retorno será um código 302 (erro e redireciona)
    def test_servico_view_nao_logado(self):
        self.client.logout()
        response = self.client.get(self.url_servico)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.url_servico}')

    # 4.6 - Testa a requisicao da view def TesteDisc(request):
    def test_teste_disc_view_logado(self):
        response = self.client.get(self.url_teste_disc)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teste-disc.html')
        
        # Verifica se os dados esperados estão sendo passados para o template teste-disc.html
        self.assertIn('obj', response.context)
        obj = response.context['obj']
        self.assertIn('dominante', obj)
        self.assertIn('influente', obj)
        self.assertIn('estavel', obj)
        self.assertIn('cauteloso', obj)
        self.assertIn('request', obj)

####### 4.7 - Classe que devolove a lista de todos os quizes: #####################
# #### class ListaQuizes(LoginRequiredMixin, ListView) - TEST OK ##################   
###################################################################################
class ListaQuizesTestCase(TestCase):

    def setUp(self):
        # Cria um usuário para simular login
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        # Cria alguns quizes usando o model_mommy
        for i in range(10):
            mommy.make(Quiz, name=f'Quiz {i}', topic=f'topic {i}')

        # URL para a página ListaQuizes
        self.url = reverse('quizes:ListaQuizes')

        # Criar requests simuladas com diferentes parâmetros de consulta GET.
        self.factory = RequestFactory()

    # 4.7.1 - Simula a busca de 10 quizes e a devolução ao template com o Login
    def test_listaquizes_view_logado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista-quizes.html')
        
        # Verifica se a lista de quizes é renderizada corretamente
        self.assertIn('quizes', response.context)
        quizes = response.context['quizes']

        # Verifica se a lista contém 10 quizes (Paginação)
        self.assertEqual(len(quizes), 10) 

    # 4.7.2 - Simula a busca de 10 quizes e a devolução ao template. Sem o login redireciona
    def test_listaquizes_nao_logado(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    # 4.7.3 - Simula a busca do quiz por NOME - def get_queryset(self):
    def test_get_queryset_with_nome(self):
        
        # Cria uma request simulada com parâmetro de consulta 'nome'
        request = self.factory.get('/lista-quizes/', {'nome': '2'})
        
        # Cria uma instância da view ListaQuizes
        view = ListaQuizes()
        view.request = request
        
        # Chama a função get_queryset
        queryset = view.get_queryset()
        
        # Verifica se a queryset retornada contém apenas os quizes com '2' no nome
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].name, 'Quiz 2')

    # 4.7.4 - Simula a busca do quiz SEM NOME - def get_queryset(self):
    def test_get_queryset_vazio(self):
        
        # Cria uma request simulada sem parâmetro de consulta 'nome'
        request = self.factory.get('/lista-quizes/')
        
        # Cria uma instância da view ListaQuizes
        view = ListaQuizes()
        view.request = request
        
        # Chama a função get_queryset
        queryset = view.get_queryset()
        # Verifica se a queryset retornada contém todos os quizzes
        self.assertEqual(len(queryset), 10)

####### 4.8 - Classe que devolove um quiz GERAL pela pk ##########################
# #### def quiz_view(request, pk): - TEST OK - url: quiz-view ####################   
##################################################################################
class QuizViewTestCase(TestCase):
    def setUp(self):
        
        # Cria um usuário para simular login
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.quiz = mommy.make(Quiz)

        #Url padrão que será chamada com a pk do quiz
        self.url = reverse('quizes:quiz-view', args=[self.quiz.pk])

    ####### 4.8.1 - Permite apenas usuários logados ########################
    def test_quiz_view_logado(self):
        # Verifica se a view só é acessível por usuários autenticados
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')
        self.assertEqual(response.context['obj'], self.quiz)

    ####### 4.8.2 - Usuários não logados, envia para tela de login #################
    def test_quiz_view_nao_logado(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')


####### 4.9 - Classe Testa envio, falha e retorno do E-mail#######################
# #### def contato(request): - TEST OK - url:quizes:contato  ####################   
##################################################################################
class ContatoViewTestCase(TestCase):
    def setUp(self):
        # Criar um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('quizes:contato')

    def test_contato_view_logado(self):
        # Verifica se a view só é acessível por usuários autenticados
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contato_view_nao_logado(self):
        # Verifica se a view redireciona usuários não autenticados para a página de login
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_contato_view_send_email_success(self):
        # Verifica se o envio de e-mail é bem-sucedido quando o formulário é válido
        self.client.force_login(self.user)
        form_data = {
            'nome': 'Nome de Teste',
            'fone': '123456789',
            'email': 'test@example.com',
            'assunto': 'Assunto de Teste',
            'mensagem': 'Mensagem de teste.'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200) #A resposta é 200 porque redireciona para a mesma página
        self.assertContains(response, 'E-mail enviado com sucesso!')  # Mensagem de sucesso presente

    def test_contato_view_send_email_error(self):
        # Verifica se o envio de e-mail falha quando o formulário é inválido
        self.client.force_login(self.user)
        form_data = {
            # Em branco para tornar o formulário inválido
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)  # Ainda renderiza a página de contato
        self.assertContains(response, 'Desculpa. Houve um erro ao enviar seu e-mail')  # Mensagem de erro presente

    def test_contato_view_form_initialization(self):
        # Verifica se o formulário é inicializado corretamente na view
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsInstance(form, ContatoForm)
        self.assertFalse(form.is_bound)  # Verifica se o formulário não está vinculado (não submetido)


####### 4.10 - Classe Testa o SALVAR e ATUALIZAR o perfil DISC do User  ##########
# #### def save_quiz_view(request, pk) - TEST OK - url:quizes:save_view ##########   
################################################################################# 
class SaveQuizViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Obrigatório um perfil vinculado ao usuário antes de realizar o teste.
        perfil = Perfil.objects.create(usuario=self.user, personalidade=1)
        self.client.login(username='testuser', password='testpass')
        
    def test_save_quiz_view_ajax(self):
        # Crie um quiz para usar nos testes
        quiz = mommy.make(Quiz)

        # Simule uma requisição AJAX para a view save_quiz_view
        url = reverse('quizes:save_view', args=[quiz.pk])
        
        csrf_token = csrf.get_token(self.client.get(url).wsgi_request)
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'tipoPersonalidade': 1,
            'scorePerfil': 80,
            'tempoDuracao': 60,
            'NomePerfil': 'Meu Perfil',
            'scoreDominante': 70,
            'scoreInfluente': 60,
            'scoreEstavel': 50,
            'scoreCauteloso': 40,
            'totalRespondido': 100,
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifique se a resposta é bem-sucedida e se o JSON de retorno é válido
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'text': 'Quiz salvo com sucesso'})

        # Verifique se o resultado foi criado corretamente no banco de dados
        result = Result.objects.get(user=self.user, quiz=quiz)
        self.assertEqual(result.scorePerfil, 80)


####### 4.11 - Classe Testa o ATUALIZAR o perfil DISC do User  ###################
# #### def atualiza_perfil(request, tipoPerfil) - TEST OK  #######################   
##################################################################################
class AtualizaPerfilTestCase(TestCase):
    def setUp(self):

        # RequestFactory cria um objeto HttpRequest para o teste.
        # Como não passa pelo Browser, dispensa um Cliente - self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.perfil = mommy.make(Perfil, usuario=self.user, personalidade=1)

    def test_atualiza_perfil(self):
        # Crie um objeto HttpRequest
        request = self.factory.get('/')
        request.user = self.user

        # Simule a chamada da função atualiza_perfil com o objeto HttpRequest
        tipo_perfil = 2
        updated_user = atualiza_perfil(request, tipo_perfil)

        # Verifique se o perfil do usuário foi atualizado corretamente
        updated_perfil = Perfil.objects.get(usuario=self.user)
        self.assertEqual(updated_perfil.personalidade, tipo_perfil)


####### 4.12 - Lista QUIZ pela pk - Uma pergunta por vez - def disc_questions(request, pk)  ########
# #### Usa ao memsmo tempo os models externos Question e Answer para montar o QUIZ #################   
####################################################################################################

#########################################################################################
####### 5. RESULT - VIEWS -                                    #####################
#########################################################################################
class ListarQuizUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    ##### 5.1 - Lista os resultados dos quizes por User - def ListarQuizUser(request) ####
    def test_listar_quiz_user(self):
        # Criar alguns objetos Result para o usuário de teste
        mommy.make(Result, user=self.user, _quantity=3)

        # Criar outro objeto Result para um usuário diferente (esse não deve ser incluído na resposta)
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        mommy.make(Result, user=other_user)

        # Fazer login com o usuário de teste
        self.client.login(username='testuser', password='testpassword')

        # Fazer uma requisição GET para a view protegida por login_required
        response = self.client.get(reverse('result:resultado'))

        # Verificar se o usuário está autenticado e redirecionado para a página correta (código de status 200)
        self.assertEqual(response.status_code, 200)

        # Verificar se todos os objetos Result criados para o usuário de teste estão presentes no contexto da resposta
        queryset = response.context['itens']
        self.assertEqual(queryset.count(), 3)

        # Verificar se o usuário associado a cada objeto Result é o usuário de teste
        for result in queryset:
            self.assertEqual(result.user, self.user)


######################################################################################
############ 5.2 - RESULT - Gerar Relatório - xhtml2 #################################
######################################################################################
class PdfDiscTestCase(TestCase):
    def setUp(self):
        # Crie um usuário de teste
        self.user = mommy.make('auth.User', username='testuser', 
        email='testuser@example.com', password='testpassword')

        # Crie um objeto Perfil associado ao usuário de teste
        self.perfil = mommy.make(Perfil, usuario=self.user)

        # Crie um objeto Result para o usuário de teste
        self.resultado = mommy.make(Result, user=self.user)

        # Crie alguns objetos Personalidade para os testes
        self.personalidades = mommy.make(Personalidade, _quantity=3)

        # Crie uma instância da classe RequestFactory
        self.factory = RequestFactory()

    def test_pdf_disc_view(self):
        # Faça login com o usuário de teste
        self.client.login(username='testuser', password='testpassword')

        # Crie um objeto HttpRequest com a URL apropriada para a view de geração do PDF
        url = reverse('result:rel-disc-pdf', args=[self.resultado.pk, self.personalidades[0].pk])
        request = self.factory.get(url)

        # Atribua o usuário de teste ao objeto HttpRequest
        request.user = self.user

        # Chame a view diretamente
        response = Pdf_Disc(request, self.resultado.pk, self.personalidades[0].pk)

        # Verifique se a resposta foi bem-sucedida (código de status 200)
        self.assertEqual(response.status_code, 200)

        # Verifique se o conteúdo da resposta é um PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')
