# Generated by Django 3.2.15 on 2022-10-27 14:05

from django.db import migrations, models
import modules.crawler.models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0027_alter_scraper_spiders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(default=modules.crawler.models.id_gen, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='groupproduct',
            name='id',
            field=models.UUIDField(default=modules.crawler.models.id_gen, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=modules.crawler.models.id_gen, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='rawproduct',
            name='id',
            field=models.UUIDField(default=modules.crawler.models.id_gen, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
