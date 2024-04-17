from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Result
from accounts.models import Perfil

#Para pegar o e-mail do user logado
from django.contrib.auth.models import User

####Para o perfil 
from personality.models import Personalidade, Definicao, Profissao

###### relatório pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

### Controle de login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

################## RESULT - Exibe apenas os RESULTADOS/quizes por usuário registrado ###################
###############################################################################################
@login_required
def ListarQuizUser(request):
   login_url = reverse_lazy('login') 
   quizes = Result.objects.filter(user=request.user).order_by('-id')
   return render(request, 'meus-quizes.html', { 'itens': quizes})


######################################################################################
############ Gerar Relatório - xhtml2 ################################################
######################################################################################
''' Esta classe facilita a geração, passando o path, um dict e o arquivo de forma estática'''
class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)
               
''' View que gera de fato o PDF - Ligada com a URL '''
@login_required    
def Pdf_Disc(request, pk, personalidade):
    login_url = reverse_lazy('login')
    pessoa = Perfil.objects.get(usuario = request.user)
    email = request.user.email
    relatorio = Result.objects.get(id=pk)
    perfil = Personalidade.objects.filter(personalidade = personalidade)
    params = {
        'usuario': pessoa,
        'email': email,
        'itens' : relatorio,
        'perfil': perfil,
        'request': request,
    }
    return Render.render('relatorio-disc.html', params, 'rel-disc')  


