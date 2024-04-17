from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.contrib import admin
from .models import Perfil


#Registrar o form 
admin.site.register(Perfil)

################################# Dispensa a criação do arquivo forms.py

class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email','first_name','last_name',)
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'
            
