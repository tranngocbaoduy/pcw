# Generated by Django 3.2.15 on 2022-10-27 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0029_auto_20221027_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id_pcw',
        ),
    ]