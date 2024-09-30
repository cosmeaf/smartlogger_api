from celery import shared_task
from subprocess import Popen

@shared_task
def start_monitoring():
    # Inicia o script de monitoramento como um processo separado
    Popen(["python3", "/root/projects/django/django_smartlogger/api/monitor/converter.py"])

@shared_task
def stop_monitoring():
    # Se o script for rodado em background, você pode matar o processo pelo PID
    # ou implementar uma forma de parar o monitoramento aqui
    pass

@shared_task
def restart_monitoring():
    # Reinicia o monitoramento
    stop_monitoring()
    start_monitoring()
