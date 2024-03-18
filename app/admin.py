# admin.py
from django.contrib import admin
from .models import QRCodeData, Profile, QRCodeScan, GiftPoint, ProfilePoint, UserGifts

# from .forms import QRCodeDataForm
import qrcode
from io import BytesIO
import base64


class QRCodeDataAdmin(admin.ModelAdmin):
    list_display = ["title", "data",  "uuid", "qr_code_image"]

    def save_model(self, request, obj, form, change):
        # Check if a new object is being created
        if (
            not obj.pk
        ):  # This will be True if the object is being created for the first time
            # Generate QR code for the newly created object
            data = obj.uuid
            print(obj)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            # Save the image to a BytesIO object
            buffer = BytesIO()
            img.save(buffer, format="PNG")

            # Encode the QR code image to base64
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            # Concatenate the base64 encoded image with the appropriate header
            qr_code_data_uri = f"data:image/jpeg;base64,{base64_image}"
            print(qr_code_data_uri)

            obj.qr_code = qr_code_data_uri

        # Call the superclass method to save the object
        super().save_model(request, obj, form, change)


admin.site.register(QRCodeData, QRCodeDataAdmin)
admin.site.register(Profile)
admin.site.register(QRCodeScan)
admin.site.register(GiftPoint)
admin.site.register(ProfilePoint)
admin.site.register(UserGifts)
