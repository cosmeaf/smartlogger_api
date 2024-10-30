from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from api.views import DeviceViewSet, EquipmentViewSet, MaintenanceViewSet,MaintenanceResetLogViewSet, EmployeeViewSet
from accounts.views import RegisterViewSet, LoginViewSet, RecoveryViewSet, OtpValidationViewSet, ResetPasswordViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="API Smartlogger",
      default_version='v1',
      description="Documentation for the API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@injetect.com.br"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'recover', RecoveryViewSet, basename='recover')
router.register(r'validate_otp', OtpValidationViewSet, basename='validate_otp')
router.register(r'reset_password', ResetPasswordViewSet, basename='reset_password')
router.register(r'devices', DeviceViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'maintenances', MaintenanceViewSet)
router.register(r'maintenance-reset-logs', MaintenanceResetLogViewSet, basename='maintenance-reset-log')
router.register(r'employees', EmployeeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(router.urls)),
]

# Handlers para páginas de erro
handler400 = 'web.views.bad_request'
handler403 = 'web.views.permission_denied'
handler404 = 'web.views.page_not_found'
handler500 = 'web.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
