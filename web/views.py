from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def solutions(request):
    return render(request, 'solutions.html')

def limitador_de_velocidade(request):
    return render(request, 'limitador_de_velocidade.html')

def router_remoto(request):
    return render(request, 'router_remoto.html')

def battery_check(request):
    return render(request, 'battery_check.html')

def contact(request):
    return render(request, 'contact.html')

def client_area(request):
    return render(request, 'client_area.html')



class PoliticaPrivacidadeView(TemplateView):
    template_name = "politica_privacidade.html"

class TermosUsoView(TemplateView):
    template_name = "termos_uso.html"

class PoliticaCookiesView(TemplateView):
    template_name = "politica_cookies.html"

class LGPDView(TemplateView):
    template_name = "lgpd.html"

class ContatoPrivacidadeView(TemplateView):
    template_name = "contato_privacidade.html"


def bad_request(request, exception):
    return render(request, 'error.html', {
        'error_code': 400,
        'error_title': 'Bad Request',
        'error_message': 'A solicitação não pôde ser processada devido a um erro de sintaxe.'
    })

def permission_denied(request, exception):
    return render(request, 'error.html', {
        'error_code': 403,
        'error_title': 'Permission Denied',
        'error_message': 'Você não tem permissão para acessar esta página.'
    })

def page_not_found(request, exception):
    return render(request, 'error.html', {
        'error_code': 404,
        'error_title': 'Page Not Found',
        'error_message': 'A página que você está procurando não foi encontrada.'
    })

def server_error(request):
    return render(request, 'error.html', {
        'error_code': 500,
        'error_title': 'Server Error',
        'error_message': 'Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde.'
    })
