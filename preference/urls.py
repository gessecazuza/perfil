#########################################################################################
####### APP - PERSONALITY - URLS.PY -           #########################################
#########################################################################################

from django.urls import path

from .views import localiza_usuario, politica_privacidade, aceitar_cookies

app_name = 'preference'

urlpatterns = [
    #path('definir_cookies', definir_cookies, name='definir_cookies'),
    path('salva-preference/', aceitar_cookies, name='aceitar_cookies'),
    path('localizacao/', localiza_usuario, name='localizacao'),
    path('politica/', politica_privacidade, name='politica'),
]
