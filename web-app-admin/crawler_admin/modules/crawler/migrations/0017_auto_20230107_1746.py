# Generated by Django 3.2.15 on 2023-01-07 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0016_auto_20230107_0650'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='groupproduct',
            options={'ordering': ['name'], 'verbose_name': 'Group Product'},
        ),
        migrations.AlterModelOptions(
            name='parser',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['group_product__name']},
        ),
        migrations.AlterModelOptions(
            name='wareparser',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='groupproduct',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crawler.category'),
        ),
        migrations.AlterField(
            model_name='sitemap',
            name='is_crawl_detail_running',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='sitemap',
            name='is_sitemap_running',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
