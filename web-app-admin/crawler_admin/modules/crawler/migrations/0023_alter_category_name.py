# Generated by Django 3.2.15 on 2022-10-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0022_auto_20221024_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
