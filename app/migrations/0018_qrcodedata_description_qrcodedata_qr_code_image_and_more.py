# Generated by Django 4.1.2 on 2024-03-17 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_profilepoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcodedata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='qrcodedata',
            name='qr_code_image',
            field=models.ImageField(default='default.png', upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='qrcodedata',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
