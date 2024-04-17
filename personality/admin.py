from django.contrib import admin

# Register your models here.
from .models import Personalidade
from .models import Definicao, Profissao, MotivadoresCarreira, ipmDisc
from .models import QuadroComparativo


#### Para as profissões terá um tab-line que permite juntar na mesma janela Perfil e Profissões

class PersonalidadeInLine(admin.TabularInline):
    model = Personalidade


class ProfissaoAdmin(admin.ModelAdmin):
    inlines = [PersonalidadeInLine]


admin.site.register(Personalidade)
admin.site.register(Profissao)
admin.site.register(Definicao)
admin.site.register(QuadroComparativo)
admin.site.register(MotivadoresCarreira)
admin.site.register(ipmDisc)
