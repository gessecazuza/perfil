from django.urls import path
from accounts.views import UsuarioCreate, PerfilUpdate

urlpatterns = [ 
    #path('', views.register, name='register'),
    path('registrar/', UsuarioCreate.as_view(), name='novo-usuario'),
    path('atualizar-dados/', PerfilUpdate.as_view(), name='atualizar-dados'), 
]