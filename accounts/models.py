from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from personality.models import Personalidade

# Create your models here.
class Perfil(models.Model):
    TIPO_SEXO_CHOICES = (
        ("MASC", ('1. MASCULINO')),
        ("FEMI", ('2. FEMININO')),
        ("TRAN", ('3. TRANSGÊNERO')),
    )
    
    CORES_PELE_CHOICES = (
        ("Branco", "Branco"), ("Negro", "Negro"),
        ("Pardo", "Mestiço/Pardo"), ("Amarelo", "Amarelo"),
        ("Morena claro", "Morena claro"),
        ("Morena escuro", "Morena escuro"), ("Ruivo", "Ruivo")
    )
    
    #70 Países
    PAISES_CHOICES = (
        ('Brasil', 'BRA - Brasil'),
        ('Afeganistão', 'AFG - Afeganistão'), (' África do Sul', 'ZAF - África do Sul'),
        ('Albânia', 'ALB - Albânia'), ('Alemanha', 'DEU - Alemanha'),
        ('Andorra', 'AND - Andorra'), ('Angola', 'AGO - Angola'),
        ('Arábia Saudita', 'SAU - Arábia Saudita'), ('Argentina', 'ARG - Argentina'),
        ('Armênia', 'ARM - Armênia'), ('Austrália', 'AUS - Austrália'),
        ('Áustria', 'AUT - Áustria'), ('Azerbaijão', 'AZE - Azerbaijão'),
        ('Bahamas', 'BHS - Bahamas'), ('Bangladesh', 'BGD - Bangladesh'),
        ('Barbados', 'BRB - Barbados'), ('Bélgica', 'BEL - Bélgica'),
        ('Bolívia', 'BOL - Bolívia'), 
        ('Canadá', 'CAN - Canadá'),  ('Chile', 'CHL - Chile'),
        ('China', 'CHN - China'),   ('Colômbia', 'COL - Colômbia'),
        ('Coreia do Sul', 'KOR - Coreia do Sul'), ('Costa Rica', 'CRI - Costa Rica'),
        ('Croácia', 'HRV - Croácia'), ('Cuba', 'CUB - Cuba'),
        ('Dinamarca', 'DNK - Dinamarca'), ('Egito', 'EGY - Egito'),
        ('Emirados Árabes', 'ARE - Emirados Árabes'), ('Equador', 'ECU - Equador'),
        ('Eslováquia', 'SVK - Eslováquia'), ('Espanha', 'ESP - Espanha'),
        ('Estados Unidos', 'USA - Estados Unidos'), ('Filipinas', 'PHL - Filipinas'),
        ('Finlândia', 'FIN - Finlândia'), ('França', 'FRA - França'),
        ('Gana', 'GHA - Gana'), ('Grécia', 'GRE - Grécia'),
        ('Holanda', 'NLD - Holanda'), ('Honduras', 'HND - Honduras'),
        ('Hungria', 'HUN - Hungria'), ('Índia', 'IND - Índia'),
        ('Indonésia', 'IDN - Indonésia'), ('Irã', 'IRN - Irã'),
        ('Iraque', 'IRQ - Iraque'), ('Irlanda', 'IRL - Irlanda'),
        ('Israel', 'ISR - Israel'), ('Itália', 'ITA - Itália'),
        ('Jamaica', 'JAM - Jamaica'), ('Japão', 'JPN - Japão'),
        ('Jordânia', 'JOR - Jordânia'), ('Líbano', 'LBN - Líbano'),
        ('Malásia', 'MYS - Malásia'),  ('Marrocos', 'MAR - Marrocos'),
        ('México', 'MEX - México'),   ('Moçambique', 'MOZ - Moçambique'),
        ('Noruega', 'NOR - Noruega'),  ('Nova Zelândia', 'NZL - Nova Zelândia'),
        ('Paquistão', 'PAK - Paquistão'), ('Peru', 'PER - Peru'),
        ('Polônia', 'POL - Polônia'),   ('Portugal', 'PRT - Portugal'),
        ('Qatar', 'QTA - Qatar'),    ('Quênia', 'KEN - Quênia'),
        ('Reino Unido', 'GBR - Reino Unido'), ('República Checa', 'CZE - República Checa'),
        ('Romênia', 'ROU - Romênia'), ('Rússia', 'RUS - Rússia'),
        ('Senegal', 'SEN - Senegal'), ('Singapura', 'SGP - Singapura'),
        ('Suécia', 'SWE - Suécia'),  ('Suíça', 'CHE - Suíça'),
        ('Tailândia', 'THA - Tailândia'),('Tanzânia', 'TZA - Tanzânia'),
        ('Turquia', 'TUR - Turquia'),  ('Ucrânia', 'UKR - Ucrânia'),
        ('Uruguai', 'URY - Uruguai'),  ('Venezuela', 'VEN - Venezuela'),
        ('Vietnã', 'VNM- Vietnã'),  ('Zâmbia', 'ZMB - Zâmbia'), 
        ('Zimbábue', 'ZWE - Zimbábue'), ('Outro', 'OUT - Outro'))

    # 100 Profissões: 25 de cada perfil em ordem numérica por perfil
    PROFISSOES_CHOICES = (
        
        # Perfil: DOMINANCIA
        ('Advogado(a)', '01-Advogado(a)'),
        ('Arquiteto(a)', '02-Arquiteto(a)'),
        ('Atleta Profissional', '03-Atleta Profissional'),
        ('CEO (Diretor Executivo)', '04-CEO (Diretor Executivo)'),
        ('Consultor(a) de Negócios', '05-Consultor(a) de Negócios'),
        ('Corretor(a) da Bolsa de Valores', '06-Corretor(a) da Bolsa de Valores'),
        ('Empresário(a)', '07-Empresário(a)'),
        ('Engenheiro(a) de Software', '08-Engenheiro(a) de Software'),
        ('Gerente de Projeto', '09-Gerente de Projeto'),
        ('Investidor(a) Financeiro(a)', '10-Investidor(a) Financeiro(a)'),
        ('Juiz(a)', '11-Juiz(a)'),
        ('Militar', '12-Militar'),
        ('Policial', '13-Policial'),
        ('Piloto(a) de Avião', '14-Piloto(a) de Avião'),
        ('Produtor(a) de Cinema', '15-Produtor(a) de Cinema'),
        ('Promotor(a) de Justiça', '16-Promotor(a) de Justiça'),
        ('Proprietário(a) de Empresa', '17-Proprietário(a) de Empresa'),
        ('Psicólogo(a) Organizacional', '18-Psicólogo(a) Organizacional'),
        ('Supervisor(a) de Produção', '19-Supervisor(a) de Produção'),
        ('Técnico(a) de Informática', '20-Técnico(a) de Informática'),
        ('Técnico(a) em Engenharia', '21-Técnico(a) em Engenharia'),
        ('Técnico(a) em Eletrônica', '22-Técnico(a) em Eletrônica'),
        ('Técnico(a) em Mecânica', '23-Técnico(a) em Mecânica'),
        ('Técnico(a) em Telecomunicações', '24-Técnico(a) em Telecomunicações'),
        ('Vendedor(a) de Alto Desempenho', '25-Vendedor(a) de Alto Desempenho'),

        # Perfil: INFLUÊNCIA
        ('Apresentador(a) de TV', '26-Apresentador(a) de TV'),
        ('Artista', '27-Artista'),
        ('Comediante', '28-Comediante'),
        ('Conselheiro(a) de Carreira', '29-Conselheiro(a) de Carreira'),
        ('Designer de Moda', '30-Designer de Moda'),
        ('Designer Gráfico(a)', '31-Designer Gráfico(a)'),
        ('Educador(a) Físico', '32-Educador(a) Físico'),
        ('Sacerdote', '33-Sacerdote/Ministro Religioso'),
        ('Escritor(a)', '34-Escritor(a)'),
        ('Promotor de Eventos', '35-Promotor de Eventos'),
        ('Fotógrafo(a)', '36-Fotógrafo(a)'),
        ('Ilustrador(a)', '37-Ilustrador(a)'),
        ('Influenciador(a) Digital', '38-Influenciador(a) Digital'),
        ('Jornalista', '39-Jornalista'),
        ('Locutor(a) de Rádio', '40-Locutor(a) de Rádio'),
        ('Maquiador(a)', '41-Maquiador(a)'),
        ('Músico(a)', '42-Músico(a)'),
        ('Pesquisador(a) de Mercado', '43-Pesquisador(a) de Mercado'),
        ('Político(a)', '44-Político(a)'),
        ('Professor(a)', '45-Professor(a)'),
        ('Psicólogo(a)', '46-Psicólogo(a)'),
        ('Relações Públicas', '47-Relações Públicas'),
        ('Repórter', '48-Repórter'),
        ('Roteirista', '49-Roteirista'),
        ('Tradutor(a)', '50-Tradutor(a)'),
        
        # Perfil: ESTABILIDADE
        ('Administrador(a)', '51-Administrador(a)'),
        ('Analista de Dados', '52-Analista de Dados'),
        ('Analista de Sistemas', '53-Analista de Sistemas'),
        ('Bibliotecário(a)', '54-Bibliotecário(a)'),
        ('Contador(a)', '55-Contador(a)'),
        ('Editor(a) de Vídeo', '56-Editor(a) de Vídeo'),
        ('Engenheiro(a) Civil', '57-Engenheiro(a) Civil'),
        ('Farmacêutico(a)', '58-Farmacêutico(a)'),
        ('Físico(a)', '59-Físico(a)'),
        ('Geólogo(a)', '60-Geólogo(a)'),
        ('Historiador(a)', '61-Historiador(a)'),
        ('Médico(a)', '62-Médico(a)'),
        ('Nutricionista', '63-Nutricionista'),
        ('Pesquisador(a) Científico', '64-Pesquisador(a) Científico'),
        ('Programador(a)', '65-Programador(a)'),
        ('Químico(a)', '66-Químico(a)'),
        ('Secretário(a) Executivo(a)', '67-Secretário(a) Executivo(a)'),
        ('Técnico(a) de Laboratório', '68-Técnico(a) de Laboratório'),
        ('Técnico(a) em Contabilidade', '69-Técnico(a) em Contabilidade'),
        ('Terapeuta Ocupacional', '70-Terapeuta Ocupacional'),

        # Perfil: CAUTELOSO
        ('Auditor(a)', '71-Auditor(a)'),
        ('Cientista de Dados', '72-Cientista de Dados'),
        ('Consultor(a) de Segurança', '73-Consultor(a) de Segurança'),
        ('Detetive Particular', '74-Detetive Particular'),
        ('Engenheiro(a) de Controle de Qualidade', '75-Engenheiro(a) de Controle de Qualidade'),
        ('Engenheiro(a) de Segurança do Trabalho', '76-Engenheiro(a) de Segurança do Trabalho'),
        ('Gerente de Qualidade', '77-Gerente de Qualidade'),
        ('Perito(a) Criminal', '78-Perito(a) Criminal'),
        ('Planejador(a) Financeiro(a)', '79-Planejador(a) Financeiro(a)'),
        ('Projetista de Software', '80-Projetista de Software'),
        ('Auditor(a) de TI', '81-Auditor(a) de TI'),
        ('Consultor(a) Jurídico', '82-Consultor(a) Jurídico'),
        ('Engenheiro(a) de Qualidade', '83-Engenheiro(a) de Qualidade'),
        ('Engenheiro(a) de Redes', '84-Engenheiro(a) de Redes'),
        ('Estatístico(a)', '85-Estatístico(a)'),
        ('Gerente de Recursos Humanos', '86-Gerente de Recursos Humanos'),
        ('Gerente de TI', '87-Gerente de TI'),
        ('Pesquisador(a) de Segurança', '88-Pesquisador(a) de Segurança'),
        ('Perito(a) Forense', '89-Perito(a) Forense'),
        ('Programador(a) de Segurança', '90-Programador(a) de Segurança'),
        ('Técnico(a) em Manutenção', '91-Técnico(a) em Manutenção'),
        ('Técnico(a) em Segurança do Trabalho', '92-Técnico(a) em Segurança do Trabalho'),
        ('Técnico(a) em Redes', '93-Técnico(a) em Redes'),
        ('Técnico(a) em Qualidade', '94-Técnico(a) em Qualidade'),
        ('Técnico(a) em TI', '95-Técnico(a) em TI'),
        ('Web Designer', '96-Web Designer'),
        ('Analista de Mercado', '97-Analista de Mercado'),
        ('Analista de Negócios', '98-Analista de Negócios'),
        ('Engenheiro(a) de Produção', '99-Engenheiro(a) de Produção'),
        ('Economista', '100-Economista'), ('Estudante', '101-Estudante'),
        ('Outra', '102-Outra') )
    
    #usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    personalidade = models.IntegerField(default=0)
    nome_completo = models.CharField(max_length=70, null=True, verbose_name="Nome completo:")
    sexo = models.CharField(max_length=5, choices=TIPO_SEXO_CHOICES, default="", verbose_name="Sexo reconhecido:")
    cpf = models.CharField(max_length=14, null=True, verbose_name="CPF:")
    nascimento = models.DateField(null=True, verbose_name="Nascimento (dd/mm/aaaa):")
    telefone = models.CharField(max_length=20, null=True, verbose_name="Telefone (Apenas dígitos - com DDD):")
    profissao = models.CharField(max_length=70, null=True, choices=PROFISSOES_CHOICES,verbose_name="Profissão/Área de Atuação:", default="")
    pais = models.CharField(max_length=50, choices=PAISES_CHOICES, default="OUTRO")
    raca_cor = models.CharField(max_length=50, choices=CORES_PELE_CHOICES, verbose_name="Cor da pele reconhecida:", default="Outro") 
    #photo = models.CharField(max_length=256, help_text="Imagem recente", null=True)
    
    def __str__(self):
        return str(self.usuario)
    
    class meta:
        verbose_name_plural = 'Perfil do Usuário'

