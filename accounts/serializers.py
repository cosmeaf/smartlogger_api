from datetime import timedelta, timezone
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .utils.client.get_client_info import get_client_info
from .utils.location.get_location_info import get_location_info
from .tasks import send_email_accounts_task
import random
import logging

logger = logging.getLogger(__name__)

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 30  # minutes


# Registro de usuário
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Endereço de e-mail já está em uso.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        # Informações do dispositivo e localização
        request = self.context.get('request')
        client_info = get_client_info(request)
        location_info = get_location_info(request.META.get('REMOTE_ADDR'))

        # Logar informações sobre o registro
        logger.info(f"Novo usuário registrado: {user.email}, Dispositivo: {client_info}, Localização: {location_info}")

        # Conteúdo do e-mail
        subject = "Bem-vindo ao nosso sistema!"
        message = f"Olá {user.first_name}, obrigado por se registrar!"
        html_message = f"""
        <html>
        <body>
            <h1>Bem-vindo ao nosso sistema!</h1>
            <p>Olá {user.first_name},</p>
            <p>Obrigado por se registrar em nossa plataforma.</p>
        </body>
        </html>
        """
        recipient_list = [user.email]
        
        # Enviar e-mail de boas-vindas de forma assíncrona
        send_email_accounts_task.delay(subject, message, recipient_list, html_message=html_message)

        return user


# Login de usuário com informações de tentativas falhas e notificação de login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("E-mail não registrado.")

        # Tenta autenticar o usuário
        user_authenticated = authenticate(username=email, password=password)
        if user_authenticated:
            # Gera os tokens JWT diretamente no serializer
            refresh = RefreshToken.for_user(user)
            
            # Captura informações da máquina e localização
            client_info = get_client_info(self.context['request'])
            ip_address = self.context['request'].META.get('REMOTE_ADDR')
            location_info = get_location_info(ip_address)

            logger.info(f"Usuário {user.email} autenticado com sucesso. Dispositivo: {client_info}, Localização: {location_info}")

            # Enviar e-mail de notificação de login
            subject = "Tentativa de login no sistema"
            message = f"""
                Olá {user.first_name},

                Houve uma tentativa de login na sua conta. Veja os detalhes abaixo:
                
                Data e Hora: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
                Dispositivo:
                    - Sistema Operacional: {client_info.get('os_name')}
                    - Versão do SO: {client_info.get('os_version')}
                    - Navegador: {client_info.get('browser')}
                    - Versão do Navegador: {client_info.get('browser_version')}
                    - Tipo de Dispositivo: {client_info.get('device_type')}
                
                Localização:
                    - IP: {ip_address}
                    - País: {location_info.get('country', 'Desconhecido')}
                    - Estado: {location_info.get('state', 'Desconhecido')}
                    - Cidade: {location_info.get('city', 'Desconhecido')}
                    - CEP: {location_info.get('zipcode', 'Desconhecido')}
                
                Caso não tenha sido você, recomendamos que altere sua senha imediatamente.

                Atenciosamente,
                Equipe de Segurança
            """
            recipient_list = [user.email]

            send_email_accounts_task.delay(subject, message, recipient_list)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }
        else:
            raise serializers.ValidationError("Credenciais inválidas.")

# Recuperação de senha por e-mail com OTP
class UserRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("E-mail não encontrado.")

        # Gerar OTP e definir expiração (10 minutos)
        otp_code = random.randint(100000, 999999)
        user.otp_code = otp_code
        user.otp_expiration = timezone.now() + timedelta(minutes=10)
        user.save()

        # Informações do dispositivo e localização
        request = self.context.get('request')
        client_info = get_client_info(request)
        location_info = get_location_info(request.META.get('REMOTE_ADDR'))

        # Logar informações da recuperação
        logger.info(f"Recuperação de senha iniciada para o usuário {user.email}. Dispositivo: {client_info}, Localização: {location_info}")

        # Conteúdo do e-mail de OTP
        subject = "Seu código OTP"
        message = f"Olá {user.first_name}, use o código {otp_code} para redefinir sua senha."
        html_message = f"""
        <html>
        <body>
            <h1>Recuperação de Senha</h1>
            <p>Olá {user.first_name},</p>
            <p>Use o código abaixo para redefinir sua senha:</p>
            <p><strong>{otp_code}</strong></p>
        </body>
        </html>
        """
        recipient_list = [user.email]
        
        # Enviar e-mail com OTP de forma assíncrona
        send_email_accounts_task.delay(subject, message, recipient_list, html_message=html_message)

        return value


# Validação de OTP com expiração
class OtpValidateSerializer(serializers.Serializer):
    otp = serializers.CharField(label="OTP", max_length=6)

    def validate(self, data):
        user = User.objects.filter(otp_code=data['otp']).first()
        if not user:
            raise serializers.ValidationError("OTP inválido ou expirado.")

        # Verificar se o OTP expirou
        current_time = timezone.now()
        if current_time > user.otp_expiration:
            raise serializers.ValidationError("O OTP expirou.")
        
        return {"message": "OTP validado com sucesso.", "user_id": user.id}


# Redefinição de senha
class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("As senhas não correspondem.")
        return attrs

    def save(self, user):
        user.set_password(self.validated_data['password'])
        user.save()

        # Informações do dispositivo e localização
        request = self.context.get('request')
        client_info = get_client_info(request)
        location_info = get_location_info(request.META.get('REMOTE_ADDR'))

        # Logar a redefinição de senha
        logger.info(f"Senha redefinida para o usuário {user.email}. Dispositivo: {client_info}, Localização: {location_info}")

        # Conteúdo do e-mail de redefinição de senha
        subject = "Senha Redefinida com Sucesso"
        message = f"Olá {user.first_name}, sua senha foi redefinida com sucesso."
        html_message = f"""
        <html>
        <body>
            <h1>Senha Redefinida</h1>
            <p>Olá {user.first_name},</p>
            <p>Sua senha foi redefinida com sucesso.</p>
        </body>
        </html>
        """
        recipient_list = [user.email]

        # Enviar notificação de redefinição de senha de forma assíncrona
        send_email_accounts_task.delay(subject, message, recipient_list, html_message=html_message)

        return {"message": "Senha redefinida com sucesso."}
