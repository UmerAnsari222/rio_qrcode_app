# Generated by Django 5.0.3 on 2024-03-12 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_qrcodedata_scanned_by_delete_qrcodescan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcodedata',
            name='scanned_by',
        ),
    ]
