# Generated by Django 4.1.2 on 2024-03-17 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_qrcodedata_description_qrcodedata_qr_code_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodedata',
            name='qr_code_image',
            field=models.ImageField(default='uploads/default.png', upload_to='uploads/'),
        ),
    ]
