from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm

from django.contrib import messages
from django.http import HttpResponseRedirect, request

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from .forms import UsuarioForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Perfil

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


################# MOdelo de registro com as Views generics ########################
class UsuarioCreate(CreateView):
    template_name = "registration/form.html" # form.html / register.html
    form_class = UsuarioForm
    success_url = reverse_lazy('login')
    
    # Valida o formulário antes de salvar 
    def form_valid(self, form):
        # Salva o formulário e pega o objeto usuário criado
        self.object = form.save()

        # Cria um perfil em branco para o usuário
        Perfil.objects.create(usuario=self.object)

        # Retorna a URL de sucesso
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "REGISTRO DE NOVO USUÁRIO"
        context['botao'] = "CADASTRAR"
        return context

@method_decorator(login_required, name='dispatch')
class PerfilUpdate(UpdateView):
    template_name = "registration/form-update.html"
    model = Perfil
    fields = ["nome_completo", "sexo", "nascimento", "profissao", 
              "telefone", "raca_cor", "pais"]
    success_url = reverse_lazy("quizes:index") # quizes:index

    # Obtém o perfil do usuário logado. Se não existir, cria um novo perfil em branco.
    def get_object(self, queryset=None):
        perfil, created = Perfil.objects.get_or_create(usuario=self.request.user)
        return perfil

    # Devolve ao template um dicionário (como request.render())
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["perfil"] = self.object  # Aqui definimos a chave 'perfil' no contexto
        context["titulo"] = "ATUALIZAÇÃO CADASTRAL"
        context["botao"] = "CONFIRMAR"
        return context