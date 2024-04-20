from django.http import HttpRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from datetime import datetime
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Quiz
from questions.models import Question, Answer
from result.models import Result
from personality.models import Personalidade, Definicao, Profissao
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from accounts.models import Perfil

####### Para tratar valores no dict
from django.utils.datastructures import MultiValueDictKeyError 

##### Para geração de relatórios PDF - xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

###### Controle de Login
from django.contrib.auth.mixins import LoginRequiredMixin #Para os generics View
from django.urls import reverse_lazy #Para redirecionar a url pós login
from django.contrib.auth.decorators import login_required #Vies com request 

######### Para envio de E-mail ######################################
from .forms import ContatoForm
from django.contrib import messages

###############################################################
# 1. Página Inicial, Sobre e Servicos - TEST OK
###############################################################
#@login_required
def IndexView(request):
    login_url = reverse_lazy('login')
    return render(request, 'index.html')
    
#@login_required
def SobreView(request):
    login_url = reverse_lazy('login')
    return render(request, 'sobre.html')

#@login_required
def ServicosView(request):
    login_url = reverse_lazy('login')
    return render(request, 'services.html')


###############################################################
# 1.4. Lista informações sobre o DISC - TEST OK - url: teste-disc
###############################################################
# @login_required
def TesteDisc(request):
    # login_url = reverse_lazy('login')
    dominante = Personalidade.objects.filter(personalidade = 1)
    influente = Personalidade.objects.filter(personalidade = 2)
    estavel = Personalidade.objects.filter(personalidade = 3)
    cauteloso = Personalidade.objects.filter(personalidade = 4)
    params = {
        'dominante': dominante,
        'influente': influente,
        'estavel': estavel,
        'cauteloso': cauteloso,
        'request': request,
    }
    return render(request, 'teste-disc.html', {'obj': params})


###############################################################
#Lista todos os quizes - Logado -  TEST OK - url: ListaQuizes
###############################################################
# LoginRequiredMixin,
class ListaQuizes(ListView):
    # login_url = reverse_lazy('login')
    model = Quiz
    template_name = 'lista-quizes.html'
    queryset = Quiz.objects.all().order_by('id')
    context_object_name = 'quizes'
    paginate_by = 10
   
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            quizes = Quiz.objects.filter(name__icontains=txt_nome)
        else:
            quizes = Quiz.objects.all()
        return quizes


######################################################################
####### Retorna um ÚNICO quiz GERAL pela pk - TEST OK - url: quiz-view
####### (Passa pelo Template lista-quizes.html para chamar os demais)
######################################################################
@login_required
def quiz_view(request, pk):
    login_url = reverse_lazy('login')
    #quiz = Quiz.objects.get(pk=pk)
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quiz.html', {'obj': quiz})


######################################################################
#SALVAR - Pega o questionário pronto via Jason pelo arquivo quizes/quiz.js
######################################################################
@login_required
def save_quiz_view(request, pk):
    login_url = reverse_lazy('login')
    try: 
        if request.is_ajax(): #Django 4.2 mudou de is_ajax() para request.is_ajax:
            data = request.POST
            token = 'csrfmiddlewaretoken' #token django - formulario recebido via request
            data_ = dict(data.lists())
            data_.pop(token) #Remove o token
            user = request.user
            quiz = Quiz.objects.get(pk=pk)
            tipo = data['tipoPersonalidade']
            dataAtual = datetime.now()
            score = data['scorePerfil']
            duration = data['tempoDuracao']
            nomePerfil = data['NomePerfil']
            dominante = data['scoreDominante']
            influente = data['scoreInfluente']
            estavel = data['scoreEstavel']
            cauteloso = data['scoreCauteloso']
            totalRespondido = data['totalRespondido']
            
            Result.objects.create(quiz=quiz,
                                user=user, 
                                scorePerfil=score,
                                personalidade=tipo, 
                                nameProfile = nomePerfil,
                                created=dataAtual, 
                                duration = duration,
                                totalAnswered = totalRespondido,
                                scoreDominante = dominante, 
                                scoreInfluente = influente,
                                scoreEstavel = estavel, 
                                scoreCauteloso = cauteloso)
            
            # Atualizar o Perfil do usuário logado
            atualiza_perfil(request, tipo)
            return JsonResponse({'text':'Quiz salvo com sucesso'})
    except MultiValueDictKeyError as e:
        return HttpResponseBadRequest("Erro ao salvar na base de dados: {}".format(e))

    # Em caso de falha, retorne um HttpResponseBadRequest ou outra resposta de erro HTTP
    return HttpResponseBadRequest("Houve falha na quisiçao ao tentar salvar.")


#################################################################################
#### Atualiza a Personalidade após salvar o teste DISC
#################################################################################
def atualiza_perfil(request, tipoPerfil):
    usuario = Perfil.objects.get(usuario=request.user)
    usuario.personalidade = tipoPerfil
    usuario.save()
    return usuario
        

######################### ############################################################
# Lista QUIZ pela pk - Uma pergunta por vez por quiz isoladamente - DISC
#####################################################################################
@login_required
def quiz_questions(request, pk):
    login_url = reverse_lazy('login')
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz_id=quiz).order_by('id')
    paginator = Paginator(questions,1)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        questions = paginator.page(page)
    except(EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)  
    return render(request, 'quiz.html', {'quiz':quiz, 'questions': questions})


##########################################################################
###################  ENVIO DE E-MAIL - TEST OK ###########################
##########################################################################
@login_required
def contato(request):
    login_url = reverse_lazy('login')
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Desculpa. Houve um erro ao enviar seu e-mail')
    context = {'form': form}
    return render(request, 'contato.html', context)


######################### ############################################################
##### Lista QUIZ pela pk - Uma pergunta por vez - disc-question.html - url: quiz-view 
##### TESTE COM ERRO: self.assertContains(response, "Pergunta:", count=num_questions)
#####################################################################################
@login_required
def disc_questions(request, pk):
    login_url = reverse_lazy('login')
    
    # Obter o objeto Quiz com base no pk em vez de usar Quiz.objects.get
    #quiz = Quiz.objects.get(id=pk)
    quiz = get_object_or_404(Quiz, id=pk) 
    questions = Question.objects.filter(quiz=quiz).order_by('id')
    paginator = Paginator(questions, 1)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)
    return render(request, 'disc-question.html', {'questions': questions, 'quiz': quiz})

######################################################################
# Monta o detalhe entre QUESTIONS  e ANSWERS pela chave pk
# Retorna um dicionário em JSON ao template quiz.html
######################################################################
''' 
@login_required
def quiz_data_view(request, pk):
    login_url = reverse_lazy('login')

    #Captura o quiz em questão pela pk
    quiz = Quiz.objects.get(pk=pk)
    totalRespostas = int(len(Answer.objects.all()))
    questions = []
    for q in quiz.get_questions(): #Um loop EXTERNO para o cabeçalho de cada pergunta
        answers = [] #Pra cada pergunta a lista de resposta é redefinida
        tipos = []
        for a in q.get_answers(): #Agora um for interno em todas as respostas de cada pergunta
            answers.append(a.text); #Add o texto de cada resposta para cada pergunta

        #Em cada pergunta um dicionário montado. A chave é a pergunta individual em str().
            E a resposta uma lista de respostas
        questions.append({str(q): answers})
       
    #Devolve um dicionário Json: 1.Perguntas e respostas; 2. O tempo máximo
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })
'''

################################################################################
# Pega uma resposta por vez via request pelo arquivo quizes/quiz.js - DISC
################################################################################
''' @login_required
def salvaResposta(request):
    if request.method == 'POST':
        data = request.POST
        dominante = data['dominante']
        influente = data['influente']
        estavel = data['estavel']
        cauteloso = data['cauteloso']
        print('Recebida via POST:', dominante)
    #return render(request, 'quiz-parcial.html', {'respostas':repostas})
    return HttpResponse('Resposta enviada')   
'''
