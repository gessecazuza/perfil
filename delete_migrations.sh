#!/bin/bash

# Comando para excluir migrações e arquivos pyc do diretório "accounts"
find . -path "accounts/migrations/*.py" -not -name "__init__.py" -delete
find . -path "accounts/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "core"
find . -path "core/migrations/*.py" -not -name "__init__.py" -delete
find . -path "core/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "perfil"
find . -path "perfil/migrations/*.py" -not -name "__init__.py" -delete
find . -path "perfil/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "personality"
find . -path "personality/migrations/*.py" -not -name "__init__.py" -delete
find . -path "personality/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "preference"
find . -path "preference/migrations/*.py" -not -name "__init__.py" -delete
find . -path "preference/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "questions"
find . -path "questions/migrations/*.py" -not -name "__init__.py" -delete
find . -path "questions/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "quizes"
find . -path "quizes/migrations/*.py" -not -name "__init__.py" -delete
find . -path "quizes/migrations/*.pyc"  -delete

# Comando para excluir migrações e arquivos pyc do diretório "result"
find . -path "result/migrations/*.py" -not -name "__init__.py" -delete
find . -path "result/migrations/*.pyc"  -delete

