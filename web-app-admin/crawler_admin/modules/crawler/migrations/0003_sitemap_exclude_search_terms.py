# Generated by Django 3.2.15 on 2023-01-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_sitemap_target_search_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemap',
            name='exclude_search_terms',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
