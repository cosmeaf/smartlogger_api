from celery import shared_task
from subprocess import Popen, PIPE
import os
import signal
import logging

# Configurar o logger
logger = logging.getLogger(__name__)

# Definir o caminho do arquivo PID e o script a ser executado
PID_FILE = '/root/projects/django/django_smartlogger/api/monitor/monitoring.pid'
SCRIPT_PATH = '/root/projects/django/django_smartlogger/api/monitor/converter.py'
PYTHON_PATH = '/root/projects/django/django_smartlogger/env/bin/python3'  # Caminho completo para o Python no ambiente virtual

@shared_task
def start_monitoring():
    """
    Inicia o processo de monitoramento, se já não estiver rodando.
    """
    if os.path.exists(PID_FILE):
        logger.info("Monitoramento já está rodando.")
        return

    try:
        # Inicia o script de monitoramento em um processo separado usando o Python do ambiente virtual
        process = Popen([PYTHON_PATH, SCRIPT_PATH], stdout=PIPE, stderr=PIPE)

        # Salva o PID do processo em um arquivo
        with open(PID_FILE, 'w') as f:
            f.write(str(process.pid))

        # Log da saída padrão e de erro do processo
        stdout, stderr = process.communicate()
        if stdout:
            logger.info(f"Saída do monitoramento: {stdout.decode().strip()}")
        if stderr:
            logger.error(f"Erro no monitoramento: {stderr.decode().strip()}")

        logger.info(f"Monitoramento iniciado com PID {process.pid}.")

    except Exception as e:
        logger.error(f"Erro ao iniciar o monitoramento: {str(e)}")


@shared_task
def stop_monitoring():
    """
    Para o processo de monitoramento utilizando o PID armazenado.
    """
    if not os.path.exists(PID_FILE):
        logger.info("Monitoramento não está rodando.")
        return

    try:
        # Lê o PID do arquivo
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        # Envia sinal de término para o processo
        os.kill(pid, signal.SIGTERM)

        # Remove o arquivo PID após parar o processo
        os.remove(PID_FILE)

        logger.info(f"Monitoramento com PID {pid} foi parado.")

    except ProcessLookupError:
        logger.warning(f"Processo com PID {pid} não encontrado.")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)  # Remove o arquivo PID se o processo não existir mais

    except Exception as e:
        logger.error(f"Erro ao parar o monitoramento: {str(e)}")


@shared_task
def restart_monitoring():
    """
    Reinicia o processo de monitoramento.
    """
    try:
        stop_monitoring()  # Para o processo atual
        start_monitoring()  # Inicia um novo processo de monitoramento

        logger.info("Monitoramento reiniciado.")

    except Exception as e:
        logger.error(f"Erro ao reiniciar o monitoramento: {str(e)}")
