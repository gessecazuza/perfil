from django.test import TestCase
from model_mommy import mommy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from quizes.forms import ContatoForm
from accounts.forms import UsuarioForm #Validar se já tem o E-mail no BD


###########################################################################
####### FORM de Envio de E-mail -                                   #######
###########################################################################
class ContatoFormTestCase(TestCase):

    # Construtor que simula um novo e-mail
    def setUp(self):
        self.nome = 'Gessé Cazuza'
        self.email = 'gessecazuza@gmail.com'
        self.fone = '11.98899.2525'
        self.assunto = 'Teste de Formulário'
        self.mensagem = 'Estamos realizando novos testes de e-mail'

        # Cria um dicionário com a mensagem:
        self.dados = {
            'nome' : self.nome,
            'email' : self.email,
            'fone' : self.fone,
            'assunto' : self.assunto,
            'mensagem' : self.mensagem
        }
       
        # Agora, criamos um novo Formulário de envio
        self.form = ContatoForm(data=self.dados)

    # Agora a classe que testará
    def test_send_mail(self):

        # Criamos o Formulário 1
        form1 = ContatoForm(data=self.dados)
        form1.is_valid()  # Foi totalmente validado?
        resp1 = form1.send_mail()  # Guarda o retorno do envio

        # Criamos o Formulário 2
        form2 = ContatoForm(data=self.dados)
        form2.is_valid()  # Foi totalmente validado?
        resp2 = form1.send_mail()  # Guarda o retorno do envio de form2

        # As duas respostas são iguais?
        self.assertEquals(resp1, resp2)

###########################################################################
####### FORM de validaçao de E-mail NÃO repetitivo                  #######
###########################################################################
class UsuarioFormTest(TestCase):
    
    def test_clean_email_with_existing_email(self):
        # Crie um usuário no banco de dados usando o django_mommy
        existing_user = mommy.make(User, email='test@example.com')

        # Crie um dicionário de dados do formulário com o mesmo email existente
        form_data = {
            'username': 'newuser',
            'email': existing_user.email,
            'password1': 'password123',
            'password2': 'password123',
        }

        # Crie uma instância do formulário com os dados do formulário
        form = UsuarioForm(data=form_data)

        # Verifique se o formulário não é válido, pois o e-mail já está cadastrado
        self.assertFalse(form.is_valid())

        # Verifique se o erro de validação esperado está presente nos erros do formulário
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "Erro! O e-mail {} já está cadastrado para outro usuário.".format(existing_user.email))

    def test_clean_email_with_new_email(self):
        # Crie um dicionário de dados do formulário com um novo e-mail
        form_data = {
            'username': 'gessecazuza',
            'email': 'gessecazuza@gmail.com',
            'password1': 'Gesse_2023',
            'password2': 'Gesse_2023',
        }

        # Crie uma instância do formulário com os dados do formulário
        form = UsuarioForm(data=form_data)

        # Verifique se o formulário é válido após tratar a exceção ValidationError
        is_valid = form.is_valid()
        if not is_valid:
            # Imprima os erros de validação para ajudar na depuração
            print(form.errors)

        self.assertTrue(is_valid)