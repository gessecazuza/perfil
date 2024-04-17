from django.urls import path
from .views import ListarQuizUser, Pdf_Disc

app_name = 'result'

urlpatterns = [

    ########### RESULTADOS por usuário
    path('resultado/', ListarQuizUser, name='resultado'),
    
    ######## DISC - Relatório PDF ############
    path('rel-disc/<pk>/<personalidade>/', Pdf_Disc, name='rel-disc-pdf'),
]