from django.contrib import admin
from .models import Preference, Cookies

# Register your models here.
class CookiesInLine(admin.TabularInline):
    model = Cookies
    
class PreferenceAdmin(admin.ModelAdmin):
    inlines = [CookiesInLine]
    
admin.site.register(Preference, PreferenceAdmin)   
admin.site.register(Cookies)

