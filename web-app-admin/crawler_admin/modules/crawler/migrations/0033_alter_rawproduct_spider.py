# Generated by Django 3.2.15 on 2022-10-29 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0032_rawproduct_spider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawproduct',
            name='spider',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='crawler.spider'),
        ),
    ]
