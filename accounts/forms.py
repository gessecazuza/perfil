from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UsuarioForm(UserCreationForm):
    
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    ''' Método de validação personalizada para garantir que um e-mail fornecido 
        em um formulário não esteja duplicado no banco de dados antes de permitir 
        que os dados sejam salvos.
    '''
    def clean_email(self):
        e = self.cleaned_data['email']
        if User.objects.filter(email=e).exists():
            raise ValidationError("Erro! O e-mail {} já está cadastrado para outro usuário.".format(e))

        return e