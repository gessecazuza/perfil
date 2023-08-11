from django.urls import path
from django.shortcuts import render

'''
    SobreView, ServicosView, ListaQuizes, disc_questions,
    quiz_view, TesteDisc, contato, save_quiz_view,
    '''
from .views import ( IndexView,
    
)


app_name = 'quizes'


urlpatterns = [

    path('', IndexView, name='index'),

]

''' 
    path('sobre/', SobreView, name='sobre'),
    path('servicos/', ServicosView, name='servico'),
    path('teste-disc/', TesteDisc, name='teste-disc'),
    path('contato/', contato, name='contato'),
    path('lista-quizes/', ListaQuizes.as_view(), name='ListaQuizes'),
    
    # Para o teste DISC - template: disc-question.html
    path('joga-disc/<pk>/', disc_questions, name='disc-view'),
    #path('joga-disc/<pk>/', DiscQuestionsView.disc_questions, name='disc-view'),
    path('joga-disc/<pk>/save/', save_quiz_view, name="save_view"),
   
    # Quizes variados - Retorna um único quiz a ser respondido pela chave pk - quiz.html
    path('lista-quizes/<pk>/', quiz_view, name='quiz-view'),
'''

handler404 = 'core.views.handler404'
