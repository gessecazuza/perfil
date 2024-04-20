# Generated by Django 4.2 on 2024-04-20 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personalidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personalidade', models.IntegerField(choices=[(1, '1. DOMINANTE'), (2, '2. INFLUENTE'), (3, '3. ESTAVEL'), (4, '4. CAUTELOSO')], default=0)),
                ('name', models.CharField(choices=[('D', 'DOMINANCIA'), ('DI', 'DOMINANCIA-INFLUÊNCIA'), ('DC', 'DOMINANCIA-CAUTELA'), ('I', 'INFLUENCIA'), ('ID', 'INFLUENCIA-DOMINÂNCIA'), ('IE', 'INFLUENCIA-ESTAVEL'), ('ESTAVEL', 'ESTABILIDADE'), ('CAUTELOSO', 'CAUTELA')], default='', max_length=30)),
                ('describe', models.CharField(help_text='Resumo sobre o perfil - 256 caracteres', max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Personalidades',
                'ordering': ['personalidade'],
            },
        ),
        migrations.CreateModel(
            name='QuadroComparativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highDimension', models.CharField(default='', help_text='Alta dimensão', max_length=100)),
                ('lowDimension', models.CharField(default='', help_text='Baixa dimensão', max_length=100)),
                ('mainFeatures', models.CharField(default='', help_text='Características principais', max_length=100)),
                ('personalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personality.personalidade')),
            ],
            options={
                'verbose_name_plural': 'Quadro Comparativo',
            },
        ),
        migrations.CreateModel(
            name='Profissao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actingArea', models.CharField(default='', help_text='Área de Atuação', max_length=1024)),
                ('profession', models.CharField(default='', help_text='Nome da Profissão', max_length=512)),
                ('description', models.CharField(default='', help_text='Descrição da Função', max_length=1024)),
                ('personalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personality.personalidade')),
            ],
            options={
                'verbose_name_plural': 'Profissões',
                'ordering': ['personalidade'],
            },
        ),
        migrations.CreateModel(
            name='MotivadoresCarreira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=1024)),
                ('howToAct', models.CharField(help_text='Como o influenciar?', max_length=1024)),
                ('personalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personality.personalidade')),
            ],
            options={
                'verbose_name_plural': 'Motivadores',
            },
        ),
        migrations.CreateModel(
            name='ipmDisc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Nome do ponto negativo reconhecido', max_length=100)),
                ('description', models.CharField(default='', help_text='Descrição do ponto negativo', max_length=512)),
                ('indice', models.DecimalField(decimal_places=2, help_text='Soma de pontos negativos', max_digits=5)),
                ('tipo_indice', models.CharField(choices=[('1', '1. NULO'), ('2', '2. MUITO BAIXO'), ('3', '3. BAIXO'), ('4', '4. NORMAL BAIXO'), ('5', '5. NORMAL'), ('6', '6. NORMAL ALTO')], default='1', max_length=20)),
                ('personalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personality.personalidade')),
            ],
            options={
                'verbose_name_plural': 'Indice de Pontos de Melhora(IPM)',
            },
        ),
        migrations.CreateModel(
            name='Definicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept', models.TextField(default='', help_text='Definição geral', max_length=1512)),
                ('strikingTraits', models.CharField(default='', help_text='Traços marcantes', max_length=1024)),
                ('characteristics', models.CharField(default='', help_text='Características marcantes', max_length=1024)),
                ('positives', models.CharField(help_text='Pontos positivos', max_length=756)),
                ('negativeTraits', models.CharField(default='', help_text='Traços negativos', max_length=1024)),
                ('limitingPoints', models.CharField(default='', help_text='Pontos limitantes', max_length=1024)),
                ('improvementPoints', models.CharField(default='', help_text='Pontos a serem melhorados', max_length=1024)),
                ('NeedsFears', models.CharField(default='', help_text='Necessidades e medos', max_length=1024)),
                ('motivatingFactors', models.CharField(default='', help_text='Fatores motivadores', max_length=1024)),
                ('teamValue', models.CharField(default='', help_text='Valor na Equipe', max_length=1024)),
                ('idealEnvironment', models.CharField(default='', help_text='Ambiente Ideal', max_length=1024)),
                ('coexistence', models.CharField(default='', help_text='Convivendo com ele... como agir?', max_length=1024)),
                ('withChallenges', models.CharField(default='', help_text='Como agem com novos desafios?', max_length=1024)),
                ('howTheyLead', models.CharField(default='', help_text='Como costumam liderar?', max_length=1024)),
                ('decisionMakin', models.CharField(default='', help_text='Como tendem a tomar decisão?', max_length=1024)),
                ('underPressure', models.CharField(default='', help_text='Sob Pressão', max_length=1024)),
                ('combinations', models.TextField(default='', help_text='Possíveis Combinações', max_length=1512)),
                ('personalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personality.personalidade')),
            ],
            options={
                'verbose_name_plural': 'Definição do Perfil',
            },
        ),
    ]
