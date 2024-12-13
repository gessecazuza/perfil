import os
import subprocess

# Caminho para o arquivo de ativação da virtualenv
activate_script_path = '/home/quizcent/virtualenv/perfil/3.10/bin/activate'

# Executar o comando chmod +x para conceder permissão de execução
subprocess.call(['chmod', '+x', activate_script_path])

# Ativar a virtualenv
activate_cmd = f'source {activate_script_path}'
subprocess.call(activate_cmd, shell=True)

"""
# Instalar django==3.2
subprocess.call(['pip', 'install', 'django==3.2']) 
subprocess.call(['pip', 'install', 'dj-database-url']) 
subprocess.call(['pip', 'install', 'dj-static'])
subprocess.call(['pip', 'install', 'django-admin-honeypot-updated-2021==1.2.0']) 


# Instalar o pacote python-dotenv
subprocess.call(['pip', 'install', 'python-dotenv'])
subprocess.call(['pip', 'install', 'python-decouple'])
subprocess.call(['pip', 'install', 'django-session-timeout'])

subprocess.call(['pip', 'install', 'django-user-agents'])
subprocess.call(['pip', 'install', 'django-bootstrap4'])

# pip install --upgrade pip
subprocess.call(['pip', 'install', 'django-stdimage'])
subprocess.call(['pip', 'install', 'gunicorn'])
subprocess.call(['pip', 'install', 'html5lib'])
subprocess.call(['pip', 'install', 'reportlab'])
subprocess.call(['pip', 'install', 'requests'])

"""
subprocess.call(['pip', 'install', 'charset-normalizer'])
subprocess.call(['pip', 'install', 'click'])
subprocess.call(['pip', 'install', 'colorama'])
subprocess.call(['pip', 'install', 'cryptography'])
subprocess.call(['pip', 'install', 'cssselect2'])
subprocess.call(['pip', 'install', 'django-braces'])
subprocess.call(['pip', 'install', 'django-cleanup'])
subprocess.call(['pip', 'install', 'django-ipware'])
subprocess.call(['pip', 'install', 'frozenlist'])
subprocess.call(['pip', 'install', 'idna'])
subprocess.call(['pip', 'install', 'lxml'])
subprocess.call(['pip', 'install', 'maxminddb'])
subprocess.call(['pip', 'install', 'multidict'])
subprocess.call(['pip', 'install', 'oscrypto'])
subprocess.call(['pip', 'install', 'packaging'])
subprocess.call(['pip', 'install', 'pillow'])
subprocess.call(['pip', 'install', 'psycopg2-binary'])
subprocess.call(['pip', 'install', 'yarl'])
subprocess.call(['pip', 'install', 'pycparser'])
subprocess.call(['pip', 'install', 'pydantic'])
subprocess.call(['pip', 'install', 'pydantic_core'])
subprocess.call(['pip', 'install', 'pyHanko'])
subprocess.call(['pip', 'install', 'pyhanko-certvalidator'])
subprocess.call(['pip', 'install', 'pypdf'])
subprocess.call(['pip', 'install', 'pypng'])
subprocess.call(['pip', 'install', 'python-bidi'])
subprocess.call(['pip', 'install', 'python-ipware'])
subprocess.call(['pip', 'install', 'pytz'])
subprocess.call(['pip', 'install', 'PyYAML'])
subprocess.call(['pip', 'install', 'qrcode'])
subprocess.call(['pip', 'install', 'user-agents'])
subprocess.call(['pip', 'install', 'urllib3'])
subprocess.call(['pip', 'install', 'xhtml2pdf'])
subprocess.call(['pip', 'install', 'webencodings'])


"""
six==1.16.0
soupsieve==2.5
sqlparse==0.5.0
static3==0.7.0
svglib==1.5.1
tinycss2==1.3.0
typing_extensions==4.11.0
tzdata==2024.1
tzlocal==5.2
ua-parser==0.18.0
uritools==4.0.2


# Desativar a virtualenv após a instalação do pacote (opcional)
# subprocess.call(['deactivate'])

# aiohttp==3.9.5 
aiosignal==1.3.1 
annotated-types==0.6.0 
arabic-reshaper==3.0.0 
asgiref==3.8.1 
asn1crypto==1.5.1
# async-timeout==4.0.3 
attrs==23.2.0 
beautifulsoup4==4.12.3 
bootstrap4==0.1.0 
certifi==2024.2.2 
cffi==1.16.0
# chardet==5.2.0
"""