from django.shortcuts import render, redirect

###### Controle de Login
from django.contrib.auth.mixins import LoginRequiredMixin #Para os generics View
from django.urls import reverse_lazy #Para redirecionar a url pós login
from django.contrib.auth.decorators import login_required #Vies com request 

######### Para envio de E-mail ######################################
#from .forms import ContatoForm
from django.contrib import messages

###############################################################
# 0. Página Error: 404
###############################################################
def handler404(request, exception):
    return render(request, '404.html', status=404)


###############################################################
# 1. Página Inicial, Sobre e Servicos - TEST OK
###############################################################
#@login_required
def IndexView(request):
    #login_url = reverse_lazy('login')
    return render(request, 'index.html')