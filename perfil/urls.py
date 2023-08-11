
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views #Importa as views de login/autenticação padrão

urlpatterns = [
    path('admin/', admin.site.urls),
    

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