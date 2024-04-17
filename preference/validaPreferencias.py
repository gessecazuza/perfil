from .models import Preference
    
def verificar_preferencias(request):
    preferencias_salvas = False
    
    if request.user.is_authenticated:
        # Confere se há preferências salvas para o usário logado
        preferencia = Preference.objects.filter(user=request.user, aceitouTermos=True).first()
        if preferencia:
           preferencias_salvas = True  
        return {
            'preferencias_salvas': preferencias_salvas
        }
    return {
            'preferencias_salvas': preferencias_salvas
        }