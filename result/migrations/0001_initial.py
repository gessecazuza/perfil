# Generated by Django 4.2 on 2023-08-10 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='Data do teste', verbose_name='Criado em:')),
                ('scorePerfil', models.FloatField(help_text='Perfil Traçado', verbose_name='Perfil Determinante (%):')),
                ('personalidade', models.IntegerField()),
                ('nameProfile', models.CharField(default='', max_length=30, verbose_name='Nome do Perfil:')),
                ('score', models.FloatField(default=1, verbose_name='Aprovação Exigida (%):')),
                ('totalAnswered', models.FloatField(default=1, verbose_name='Total respondido (%):')),
                ('duration', models.FloatField(default=1)),
                ('scoreDominante', models.FloatField(default=1, help_text='Nota Perfil Dominante')),
                ('scoreInfluente', models.FloatField(default=1, help_text='Nota Perfil Influente')),
                ('scoreEstavel', models.FloatField(default=1, help_text='Nota Perfil Estável')),
                ('scoreCauteloso', models.FloatField(default=1, help_text='Nota Perfil Cauteloso')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Resultados',
            },
        ),
    ]
