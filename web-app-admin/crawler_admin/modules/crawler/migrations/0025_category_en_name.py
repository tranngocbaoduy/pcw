# Generated by Django 3.2.15 on 2022-10-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0024_category_vi_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="en_name",
            field=models.CharField(blank=True, default="", max_length=250, null=True),
        ),
    ]
