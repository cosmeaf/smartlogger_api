from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer, 
    UserRecoverySerializer, 
    OtpValidateSerializer, 
    UserResetPasswordSerializer
)


logger = logging.getLogger(__name__)

        
class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro no registro: {str(e)}")
            return Response({"errors": "Unable to process request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            # Valida e retorna os dados diretamente do serializer
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro no login: {str(e)}")
            return Response({"errors": "Login failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecoveryViewSet(viewsets.ViewSet):
    serializer_class = UserRecoverySerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro na recuperação de senha: {str(e)}")
            return Response({"errors": "Recovery failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtpValidationViewSet(viewsets.ViewSet):
    serializer_class = OtpValidateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro na validação de OTP: {str(e)}")
            return Response({"errors": "OTP validation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = UserResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro na redefinição de senha: {str(e)}")
            return Response({"errors": "Reset password failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
