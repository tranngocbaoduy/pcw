# Generated by Django 3.2.15 on 2023-01-07 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0015_auto_20230107_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemap',
            name='is_crawl_detail_running',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sitemap',
            name='is_sitemap_running',
            field=models.BooleanField(default=False),
        ),
    ]
