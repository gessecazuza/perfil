
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views #Importa as views de login/autenticação padrão

""" SESSÃO 26 -  Proteja seu painel de administração e registre tentativas de hacking
    162. - Criar um falso painel de ADM (honney_pot)

    Criar um falso painel de ADM, permite indentificar o IP, usuário, data e quantas vezes tentou.

    > 1: Alterar a url padrao admin para dificultar o acesso ao painel ADM, exemplo: masteradmin; 
    > 2: Implementar um honeypot de administração do Django para duplicar um painel de administração.

        pip install django-admin-honneypot
        pip install django-admin-honeypot-updated-2021 (Versao 4 Django)

      >  No settings.py add o aplicativo 'admin_honeypot'
      > Gerar uma segunda url de redirecionamento  (admin_honeypot.urls) no path;
        # Esta Enviará a solicitação para uma tabela do honeypot de administrador;
        # Registrará o endereço IP desse usuário e o número de vezes que ele tentou fazer login
      > Rodar o migrate para criar esta nova tabela de registro (py manage.py migrate)
      > Rodar o servidor para teste: py manage.py runserver. 
      >> Notar que gera-se um falso form de login para enganar o invasor, com a url admin/
      > No verdadeiro painel ADM, uma tabela 'Login attempts' guardou os detalhes do login errôneo.
"""

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('masteradmin/', admin.site.urls),
    

    #usando as rotas padrôes para login
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', include('accounts.urls')),

     #Inclui a url dos questionários (quizes)
    path('', include('quizes.urls', namespace='quizes')),

    #Inclui a url das prefencias (preference)
    path('', include('preference.urls', namespace='preference')),

    #Inclui as urls de result (relatório PDF)
    path('', include('result.urls', namespace='result')),

    #path('', include('core.urls')),
]
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto