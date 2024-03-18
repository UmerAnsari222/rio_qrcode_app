from django.db import models
import uuid
from django.contrib.auth.models import User


class QRCodeData(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    data = models.IntegerField()
    qr_code = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    qr_code_image = models.ImageField(
        upload_to="uploads/", default="uploads/default.png")

    def __str__(self):
        return str(self.title)


class QRCodeScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCodeData, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user.username}-{self.qr_code.data}")


class ProfilePoint(models.Model):
    profile_points = models.IntegerField()
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)


class GiftPoint(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    gift_points = models.IntegerField()
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    qr_code_image = models.ImageField(
        upload_to="gifts/", default="gifts/default.png")

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    username = models.CharField(max_length=255)
    points = models.IntegerField()
    qr_code = models.TextField(blank=True, null=True)
    scanned_by_admin = models.BooleanField(default=False)
    # gifts = models.ForeignKey(GiftPoint, blank=True,
    #                           null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)


class UserGifts(models.Model):
    user = models.ForeignKey(User, blank=True,
                             null=True, on_delete=models.CASCADE)
    gifts = models.ForeignKey(GiftPoint, blank=True,
                              null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.gifts.name
