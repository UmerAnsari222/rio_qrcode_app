# Generated by Django 5.0.3 on 2024-03-09 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_qrcodedata_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodedata',
            name='qr_code',
            field=models.TextField(blank=True, null=True),
        ),
    ]