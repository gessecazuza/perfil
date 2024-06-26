"""
Django settings for perfil project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

""" Sessão 26 - CONFIGURAÇÕES DE SEGURANÇA -
    161. Armazene as informações confidenciais do seu site com segurança

    1. Ocultar informações importantes do projeto em arquivo .env ou .ini que não devem ser entregues no deploy.
        Ex.: A SECRET_KEY, o tipo de DEBUG, o nome do BD, etc.
    2. Podemos usar um pacote para auxiliar nisso: pip install python-decouple, que permite gerar 
        uma separação estrita entre configurações e código (https://pypi.org/project/python-decouple/);
    3. Importar o pacote (from decouple import config);
    4. Criar um novo arquivo e nomeá-lo como ponto env, na raiz do projeto;
    5. Copiar as variáveis que serão protegidas, sem espaços em branco: 
        SECRET_KEY, DEBUG, BD, Config de Email
    6. Para acessar as variáveis, usar: SECRET_KEY = config('SECRET_KEY'), por exemplo.
    7. Incluir este arquivo .env dentro do arquivo gitignore NÃO enviar o código para o GitHub;
    8. Criar um segundo arquivo de exemplo para demonstrar apenas as chaves pra quem o receber .env-sample;
        Remover os valores da chaves que servirão como amostra apenas para um download, por exemplo.
        > Podemos enviar esse código de exemplo de ambiente, arquivo de exemplo, para o GitHub (.env-sample).
"""

from pathlib import Path                                    # Padrão para acessar o caminho da aplicação
import os                                                   # Acessar o Sistema Operacional
from django.contrib.messages import constants as messages   # Sistema de mensagens
from decouple import config                                 # Pacote de configuração de segurança
from dotenv import load_dotenv                              # pip install python-dotenv

SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS  = ['*'] # 35.94.14.109, quizcenter.com.br

# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

## 1. Se não tiver valor, será True. 2. Precisa receber um Booleano  
DEBUG = config('DEBUG', default=False, cast=bool) 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Com a pasta static no mesmo nível da pasta do projeto - D:\perfil\perfil\static
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'static' # Onde serão coletados os static (python manage.py collectstatic)

#Arquivos de Mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

#Para coletar os arquivos css, js e imagens na pasta 'D:\perfil\static'
# python manage.py collectstatic
STATICFILES_DIRS = [
    'perfil/static/'
]
print("Estáticos: ", STATICFILES_DIRS)

# Application definition
INSTALLED_APPS = [
       
   #usar o login padrão - Exigido como primeiro app da lista 
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_user_agents',
    'bootstrap4', 
    
   #######################################################
    #Ativa os módulos dos apps (arquivo apps.py de cada um)
    ##################################################
    'quizes.apps.QuizesConfig',
    'questions.apps.QuestionsConfig',
    'result.apps.ResultConfig',
    'personality.apps.PersonalityConfig',
    'preference.apps.PreferenceConfig',
     'admin_honeypot', # Aula 162. Gerar Falso painel de adminsitração
]

""" Sessão 26 - Segurança - Aula 163. Sair automaticamente após inatividade
    1.> pip install django-session-timeout 
    2. Adicionar a chave MIDDLEWARE: 'django_session_timeout.middleware.SessionTimeoutMiddleware',
    3. Criar a variável de sessão com o tempo: SESSION_EXPIRE_SECONDS = 3600  # 1 hora de sessão
"""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Definirá um is_ajax método em cada solicitação antes de ser recebido pela exibição.
    'quizes.middlewares.AjaxMiddleware', 
    'django_session_timeout.middleware.SessionTimeoutMiddleware', ## Determinar tempo para sessão
]

############### Controle de sessão ###################################
SESSION_EXPIRE_SECONDS = 3600               # 1 hora de sessão: 3600s
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True   # Derruba se tiver inativo
SESSION_TIMEOUT_REDIRECT = 'accounts/login' # Redirecionar ao login

ROOT_URLCONF = 'perfil.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ### Validador automatico do app Preference
                'preference.validaPreferencias.verificar_preferencias', 
            ],
        },
    },
]

WSGI_APPLICATION = 'perfil.wsgi.application'

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se a variável de ambiente para a engine do banco de dados SQLite está definida
if os.getenv("DATABASE_ENGINE") == 'django.db.backends.sqlite3':
    # Se definida, use o SQLite como banco de dados
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DATABASE_ENGINE"),
            "NAME": os.getenv("DATABASE_NAME"),
        }
    }
else:
    # Se não definida ou se a engine não for sqlite3, use as configurações para o PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DATABASE_ENGINE"),
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD"),
            "HOST": os.getenv("DATABASE_HOST"),
            "PORT": os.getenv("DATABASE_PORT"),
        }
    }

# Banco de dados GeoLite2-City.mmdb para geolocalização
# GEOIP_PATH = os.path.join(BASE_DIR, 'localizacao\GeoLite2-City.mmdb') # D:\perfil\localizacao\


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

#Sistema de autenticação personalizado
#AUTH_USER_MODEL = 'usuarios.CustomUsuario'

#Enviar email com token via terminal
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SMTP configuraçao de segurança
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

### Configurações de autenticação - São três constantes exigidas
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'quizes:index'
LOGOUT_REDIRECT_URL = 'quizes:index'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

