# Generated by Django 3.2.15 on 2022-10-24 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0026_alter_scraper_spiders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='spiders',
            field=models.ManyToManyField(through='crawler.ScraperSpider', to='crawler.Spider'),
        ),
    ]