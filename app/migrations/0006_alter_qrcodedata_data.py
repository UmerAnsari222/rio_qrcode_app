# Generated by Django 5.0.3 on 2024-03-09 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_qrcodedata_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodedata',
            name='data',
            field=models.IntegerField(),
        ),
    ]
