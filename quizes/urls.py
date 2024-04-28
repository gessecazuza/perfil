from django.urls import path
from .views import (
    IndexView, SobreView, ServicosView, ListaQuizes, disc_questions,
    TesteDisc, contato, save_quiz_view, quiz_questions,
)

app_name = 'quizes'

urlpatterns = [
   
    path('', IndexView, name='index'),
    path('sobre/', SobreView, name='sobre'),
    path('servicos/', ServicosView, name='servico'),
    path('teste-disc/', TesteDisc, name='teste-disc'),
    path('contato/', contato, name='contato'),
    path('lista-quizes/', ListaQuizes.as_view(), name='ListaQuizes'),
    
    # Para o teste DISC - template: disc-question.html
    path('joga-disc/<pk>/', disc_questions, name='disc-view'),
    
    path('joga-disc/<pk>/save/', save_quiz_view, name="save_view"),
   
   # Para o teste DISC - template: quiz-question.html
    path('joga-quiz/<pk>/', quiz_questions, name='quiz-view'),

]
