from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define as configurações padrão do Django para o módulo 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Carrega as configurações do Django para o Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tarefas de apps Django
app.autodiscover_tasks()
