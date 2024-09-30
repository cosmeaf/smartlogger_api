from django.urls import path
from .views import (
    PoliticaPrivacidadeView, 
    TermosUsoView, 
    PoliticaCookiesView, 
    LGPDView, 
    ContatoPrivacidadeView,
    home, 
    about, 
    solutions, 
    limitador_de_velocidade, 
    router_remoto, 
    battery_check, 
    contact, 
    client_area
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('solutions/', solutions, name='solutions'),
    path('solutions/limitador-de-velocidade/', limitador_de_velocidade, name='limitador_de_velocidade'),
    path('solutions/router-remoto/', router_remoto, name='router_remoto'),
    path('solutions/battery-check/', battery_check, name='battery_check'),
    path('contact/', contact, name='contact'),
    path('client-area/', client_area, name='client_area'),
    path('politica-privacidade/', PoliticaPrivacidadeView.as_view(), name='politica_privacidade'),
    path('termos-de-uso/', TermosUsoView.as_view(), name='termos_uso'),
    path('politica-de-cookies/', PoliticaCookiesView.as_view(), name='politica_cookies'),
    path('lgpd/', LGPDView.as_view(), name='lgpd'),
    path('contato-privacidade/', ContatoPrivacidadeView.as_view(), name='contato_privacidade'),
]
