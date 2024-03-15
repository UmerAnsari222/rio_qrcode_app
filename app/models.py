from django.db import models
import uuid
from django.contrib.auth.models import User


class QRCodeData(models.Model):
    data = models.IntegerField()
    qr_code = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.data)


class QRCodeScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCodeData, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user.username}-{self.qr_code.data}")


class Profile(models.Model):
    username = models.CharField(max_length=255)
    points = models.IntegerField()
    qr_code = models.TextField(blank=True, null=True)
    scanned_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


class ProfilePoint(models.Model):
    profile_points = models.IntegerField()
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)


class GiftPoint(models.Model):
    gift_points = models.IntegerField()
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
