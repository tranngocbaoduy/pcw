# Generated by Django 4.1.3 on 2023-01-27 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0021_product_is_subscribe"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_used",
            field=models.BooleanField(default=False),
        ),
    ]