from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, subject, message, recipient_list, from_email=None, html_message=None):
        """
        Classe para envio de e-mail.

        :param subject: Assunto do e-mail.
        :param message: Corpo do e-mail em texto simples.
        :param recipient_list: Lista de destinatários.
        :param from_email: Remetente (opcional, se não fornecido, usa o DEFAULT_FROM_EMAIL).
        :param html_message: Corpo do e-mail em HTML (opcional).
        """
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.html_message = html_message

    def send(self):
        """Método para enviar o e-mail."""
        try:
            # Verifica se um corpo de HTML foi passado
            if self.html_message:
                email = EmailMultiAlternatives(self.subject, self.message, self.from_email, self.recipient_list)
                email.attach_alternative(self.html_message, "text/html")
                email.send()
            else:
                send_mail(self.subject, self.message, self.from_email, self.recipient_list)
            logger.info(f"E-mail enviado com sucesso para {self.recipient_list}")
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {self.recipient_list}: {e}")
            raise e

    def log_to_console(self):
        """Método para logar o e-mail no console em vez de enviá-lo."""
        logger.info(f"E-mail (SIMULAÇÃO) enviado para {self.recipient_list}")
        logger.info(f"Assunto: {self.subject}")
        logger.info(f"Mensagem: {self.message}")
        if self.html_message:
            logger.info(f"Mensagem HTML: {self.html_message}")


@shared_task
def send_email_accounts_task(subject, message, recipient_list, from_email=None, html_message=None):
    """
    Task Celery para envio de e-mails usando a classe EmailSender.
    A forma de envio (real ou simulado no console) pode depender do ambiente de execução.
    """
    email_sender = EmailSender(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=from_email,
        html_message=html_message
    )

    # Se estiver em modo de desenvolvimento (logar no console), caso contrário, enviar o e-mail
    if settings.DEBUG:  # Para desenvolvimento, podemos simular o envio logando no console
        email_sender.log_to_console()
    else:
        email_sender.send()  # Envia o e-mail no ambiente de produção
