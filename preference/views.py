from django.conf import settings #Arquivo settings.py
from .models import Preference, Cookies
from datetime import datetime

#Permite armazenar uma instância de usuário anônimo
from django.contrib.auth.models import AnonymousUser

# Para dados do cliente (agente em uso - pip install django_user_agents)
from django_user_agents.utils import get_user_agent

# Base de dados GeoLite2-City.mmdb (pip install geoip2)
import geoip2.database
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError, GeoIP2Error
import socket

# Alternativa para capturar dados da plataforma
import platform
from django.utils.datastructures import MultiValueDictKeyError

#Para requisição via POST
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# usado para manipular endereços IP
import ipaddress


def politica_privacidade(request):
    return render(request, 'politica.html')


######################################################################
## SALVAR - Pega as preferências aceitas, com dados do terminal    ##
######################################################################
''' BUSCA FEITA DIRETO NO ARQUIVO SETTINGS.PY
    1. Antes de gravar a preferencia, buscar: 
    a) User, IP e Aceitou termos;
    2. Se NAO tem, exibir mensagem no template e deixar gravar
        2. SE já tem NÃO exibir o form no index.html'''
def aceitar_cookies(request):
    if request.method == 'POST':
        
        # Capturando os parâmetros do formulário   
        aceitouTermos = True
        analytics_cookies = True if 'analytics_cookies' in request.POST else False
        marketing_cookies = True if 'marketing_cookies' in request.POST else False

        # Obter o endereço IP do cliente
        ipPesquisado = request.META.get('HTTP_X_FORWARDED_FOR')
        if ipPesquisado:
            ipTerminal = ipPesquisado.split(',')[0].strip()  # Remover espaços em branco extras
        elif 'REMOTE_ADDR' in request.META:
            ipTerminal = request.META['REMOTE_ADDR'].strip()  # Remover espaços em branco extras
        else:
            ipTerminal = None  # ou defina um valor padrão se nenhum IP for encontrado
        # Verificar se o IP é válido
        if ipTerminal:
            try:
                ipaddress.ip_address(ipTerminal)  # Isso irá levantar uma exceção se o IP não for válido
            except ValueError:
                # Trate o caso em que o IP não é válido
                ipTerminal = None

        usuario = request.user

        ##### Buscar no banco de dados ####
        preferencia = Preference.objects.filter(user=usuario, ipTerminal=ip, aceitouTermos=True).first()
        
        if not preferencia:
            # Acessando a constante GEOIP_PATH definida no arquivo settings.py
            geoip_path = settings.GEOIP_PATH
            navegador = get_user_agent(request)
            so = platform.system()
            versaoOS = platform.release()
            arquitetura = platform.machine()          
            processador = platform.processor()
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if language:
                idioma = language.split(',')[0]
            else:
                idioma = 'Desconhecido'
            dataAdesao = datetime.now()
            hora = f"{dataAdesao.strftime('%d/%m/%Y')} - {dataAdesao.strftime('%H:%M:%S')}"
            
            ### Ponteiro que varre o BASE de dados
            reader = geoip2.database.Reader(geoip_path)
            try:
                response = reader.city(ipTerminal)
                country = response.country.name                
                city = response.city.name
            except (AddressNotFoundError, GeoIP2Error):
                country = 'Desconhecido'
                city = 'Não localizada' # Fechando o leitor de banco de dados
            reader.close()  # Fechando o leitor de banco de dados
            '''if request.user.is_anonymous:
                usuario = Preference.objects.create(user=None, aceitouTermos = aceitouTermos)
            else:
                usuario = Preference.objects.create(user=request.user,  aceitouTermos = aceitouTermos)
            '''
            Preference.objects.create(
                user=usuario, dataAdesao=dataAdesao, SO=so,
                VersaoSO=versaoOS, arquitetura=arquitetura, processador=processador,
                navegador=navegador,  ipTerminal=ipTerminal, pais=country, 
                cidade=city, idioma=idioma, aceitouTermos=aceitouTermos,
                analyticsCookies = analytics_cookies, marketingCookies = marketing_cookies 
            )
            # Redirecionando de volta para o index.html
        return render(request, 'index.html', {'preferencias_salvas': True})
    return render(request, 'index.html', {'preferencias_salvas': False})

""" 
def aceitar_cookies_old(request):
    if request.method == 'POST':
        
        # Capturando os parâmetros do formulário   
        aceitouTermos = True
        analytics_cookies = True if 'analytics_cookies' in request.POST else False
        marketing_cookies = True if 'marketing_cookies' in request.POST else False

        # Obter o endereço IP do cliente
        ipPesquisado = request.META.get('HTTP_X_FORWARDED_FOR')
        if ipPesquisado:
            ipTerminal = ipPesquisado.split(',')[0]
        else:
            ipTerminal = request.META.get('REMOTE_ADDR')
        ip = ipTerminal
        usuario = request.user

        ##### Buscar no banco de dados ####
        preferencia = Preference.objects.filter(user=usuario, ipTerminal=ip, aceitouTermos=True).first()
        
        if not preferencia:
            # Acessando a constante GEOIP_PATH definida no arquivo settings.py
            geoip_path = settings.GEOIP_PATH
            navegador = get_user_agent(request)
            so = platform.system()
            versaoOS = platform.release()
            arquitetura = platform.machine()          
            processador = platform.processor()
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if language:
                idioma = language.split(',')[0]
            else:
                idioma = 'Desconhecido'
            dataAdesao = datetime.now()
            hora = f"{dataAdesao.strftime('%d/%m/%Y')} - {dataAdesao.strftime('%H:%M:%S')}"
            
            ### Ponteiro que varre o BASE de dados
            reader = geoip2.database.Reader(geoip_path)
            try:
                response = reader.city(ipTerminal)
                country = response.country.name                
                city = response.city.name
            except (AddressNotFoundError, GeoIP2Error):
                country = 'Desconhecido'
                city = 'Não localizada' # Fechando o leitor de banco de dados
            reader.close()  # Fechando o leitor de banco de dados
            '''if request.user.is_anonymous:
                usuario = Preference.objects.create(user=None, aceitouTermos = aceitouTermos)
            else:
                usuario = Preference.objects.create(user=request.user,  aceitouTermos = aceitouTermos)
            '''
            Preference.objects.create(
                user=usuario, dataAdesao=dataAdesao, SO=so,
                VersaoSO=versaoOS, arquitetura=arquitetura, processador=processador,
                navegador=navegador,  ipTerminal=ipTerminal, pais=country, 
                cidade=city, idioma=idioma, aceitouTermos=aceitouTermos,
                analyticsCookies = analytics_cookies, marketingCookies = marketing_cookies 
            )
            # Redirecionando de volta para o index.html
        return render(request, 'index.html', {'preferencias_salvas': True})
    return render(request, 'index.html', {'preferencias_salvas': False})
"""

###### Carrega os dados do terminal ########
@login_required        
def localiza_usuario(request):

    # Definir parametros como um dicionário vazio no início
    parametros = {}
    
    # Obter o endereço IP do cliente. Se não o encontrar: IP Desconhecido
    ipTerminal = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ipTerminal:
        ipTerminal = ipTerminal.split(',')[0]
    else:
        ipTerminal = request.META.get('REMOTE_ADDR', 'IP Desconhecido')

    usuario = request.user
    ##### Buscar no banco de dados ####
    preferencia = Preference.objects.filter(user=usuario, ipTerminal=ipTerminal, aceitouTermos=True).first()
    
    if preferencia:
        
        # Acessando a constante GEOIP_PATH definida no arquivo settings.py
        # D:\QuizCenter\quiz_proj\settings.py
        geoip_path = settings.GEOIP_PATH
    
        # Capturando o agente do usuário
        #navegador = get_user_agent(request)
        navegador = preferencia.navegador
            
        # Capturando a plataforma do cliente
        SO = preferencia.SO

        # Capturando a versão da plataforma do cliente
        versaoOS =  preferencia.VersaoSO
        arquitetura =preferencia.arquitetura
        processador = preferencia.processador.split(',')[0]
      
        # Obter o idioma do cliente
        idioma = preferencia.idioma.split(',')[0]
        
        # Capturando a data e hora da requisição   
        now = preferencia.dataAdesao
        hora = f"{now.strftime('%d/%m/%Y')} - {now.strftime('%H:%M:%S')}"

        aceitouTermos =  preferencia.aceitouTermos
        marketing    =  preferencia.marketingCookies
        analiticos   =  preferencia.analyticsCookies
        
        # Ponteiro que varre o BASE de dados
        reader = geoip2.database.Reader(geoip_path)
        try:
            response = reader.city(ipTerminal)
            country = response.country.name
            city = response.city.name
        except (AddressNotFoundError, GeoIP2Error):
            country = 'Desconhecido'
            city = 'Não localizada'

        # Fechando o leitor de banco de dados
        reader.close()

        # Criando o dicionário de parâmetros
        parametros = {
            'usuario': usuario,
            'ipTerminal': ipTerminal,
            'SO': SO,
            'VersaoOS': versaoOS,
            'arquitetura': arquitetura,
            'processador': processador,
            'terminal': navegador,
            'idioma': idioma,
            'now': hora,
            'aceitouTermos': aceitouTermos,
            'marketing': marketing,
            'analiticos': analiticos,
            'pais': country,
            'cidade': city,
        }
    else:
        # Mensagem de erro para o usuário sem preferências registradas
        parametros['error_message'] = "Usuário sem termos de privacidade registrados."
        #messages.error ="Usuário sem termos de privacidade registrados."      
    
    # Renderizando o template e passando os parâmetros para o contexto
    return render(request, 'localizacao.html', {'dados': parametros})
