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
    template_name = "registration/form.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    #Valida o formulário antes de salvar 
    def form_valid(self, form):
        '''Antes de criar, podemos definir a que grupo pertence'''
        #grupo = get_object_or_404(Group, name="Docente")
        
        #Valida e Cria o usuário de fato (objeto)
        url = super().form_valid(form)
        
        '''Salva no grupo indicado'''
        #self.object.groups.add(grupo)
        self.object.save()
        
        #Cria um perfil para o usuário com os campos padrões nulos (null=True)
        Perfil.objects.create(usuario=self.object)
        return url  #devolva à url do reverse_lazy
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "REGISTRO DE NOVO USUARIO"
        context['botao'] = "CADASTRAR"
        return context

@method_decorator(login_required, name='dispatch')
class PerfilUpdate(UpdateView):
    template_name = "registration/form-update.html"
    model = Perfil
    fields = ["nome_completo", "sexo", "nascimento", "profissao", 
              "telefone", "raca_cor", "pais"]
    success_url = reverse_lazy("quizes:index")

    # obter um Perfil já existente ou retornar um erro 404 caso ele não seja encontrado. 
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Perfil, usuario=self.request.user)
        return self.object

    #Devolve ao template um dicionário (como request.render())
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["perfil"] = self.object  # Aqui definimos a chave 'perfil' no contexto
        context["titulo"] = "ATUALIZAÇÃO CADASTRAL"
        context["botao"] = "CONFIRMAR"
        return context