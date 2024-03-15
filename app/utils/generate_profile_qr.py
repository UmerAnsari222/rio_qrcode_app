import qrcode
from io import BytesIO
import base64


def generate_profile_qr_code(data):
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
    return qr_code_data_uri
