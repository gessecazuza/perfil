# Generated by Django 4.2 on 2024-04-20 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Título - 200 caracteres', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('points', models.FloatField(default=0, help_text='Valor da questão')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
            ],
            options={
                'verbose_name_plural': 'Questões',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Alternativa - 120 caracteres', max_length=120)),
                ('correct', models.BooleanField(default=False, help_text='Resposta certa?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
            ],
            options={
                'verbose_name_plural': 'Alternativas',
            },
        ),
    ]
