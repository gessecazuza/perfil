# Generated by Django 4.2 on 2023-08-10 02:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataAdesao', models.DateTimeField(auto_now_add=True)),
                ('SO', models.CharField(default='Windows', max_length=50)),
                ('VersaoSO', models.CharField(default='', max_length=50)),
                ('arquitetura', models.CharField(default='', max_length=50)),
                ('processador', models.CharField(default='', max_length=50)),
                ('navegador', models.CharField(default='', max_length=70)),
                ('ipTerminal', models.CharField(default='', max_length=30)),
                ('pais', models.CharField(default='', max_length=70)),
                ('cidade', models.CharField(default='', max_length=70)),
                ('idioma', models.CharField(default='', max_length=50)),
                ('aceitouTermos', models.BooleanField(default=True)),
                ('analyticsCookies', models.BooleanField(default=False)),
                ('marketingCookies', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Preferências',
            },
        ),
        migrations.CreateModel(
            name='Cookies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoCookie', models.CharField(choices=[('0. RECUSADO', 'RECUSADO'), ('1. OBRIGATORIO', 'OBRIGATORIO'), ('2. PREFERENCIAS', 'PREFERENCIAS'), ('3. ESTATICOS', 'ESTATISTICOS'), ('4. MARKETING', 'MARKETING')], default='OBRIGATORIO', max_length=30)),
                ('descricao', models.CharField(choices=[('RECUSADO', 'Cliente recusou os termos de gravação.'), ('OBRIGATORIO', 'Cookies necessários para geração do teste DISC.'), ('PREFERENCIAS', 'Cliente pode definir os que deseja gravar.'), ('ESTATICOS', 'Permite colher dados de uso, tempo, e conteúdo da navegação.'), ('MARKETING', 'Permite campanhas de marketing para melhorar relacionamento e ofertas.')], default='', max_length=256)),
                ('durationCookie', models.DateTimeField(default=datetime.datetime(2023, 8, 17, 2, 59, 38, 969698, tzinfo=datetime.timezone.utc), null=True)),
                ('preferencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preference.preference')),
            ],
            options={
                'verbose_name_plural': 'Cookies',
            },
        ),
    ]
