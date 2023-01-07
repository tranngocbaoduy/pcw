# Generated by Django 3.2.15 on 2023-01-05 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_rename_spider_parser_ware_parser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parser',
            name='ware_parser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parsers', to='crawler.wareparser'),
        ),
    ]