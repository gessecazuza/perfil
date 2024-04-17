'''
Ao implementar is_ajax em seu projeto e tem um escopo amplo, aqui está uma maneira 
de implementar is_ajax a cada solicitação automaticamente:

1. crie um middlewares.pyem qualquer um dos seus aplicativos, no meu caso, quizes. 
(não importa em qual aplicativo você adiciona isso, middlewares são funções wrapper chamadas 
globalmente para executar ações antes ou depois da exibição). 
    isso definirá um is_ajaxmétodo em cada solicitação antes de ser recebido pela exibição.

2. conecte isso settings.py:

MIDDLEWARE = [
    'quizes.middlewares.AjaxMiddleware', 
]

https://stackoverflow.com/questions/70419441/attributeerror-wsgirequest-object-has-no-attribute-is-ajax
'''

class AjaxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def is_ajax(self):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
        request.is_ajax = is_ajax.__get__(request)
        response = self.get_response(request)
        return response