from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
