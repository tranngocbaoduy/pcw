# Generated by Django 3.2.15 on 2022-10-24 12:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0021_auto_20221023_0456"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256)),
                ("address", models.CharField(blank=True, max_length=256, null=True)),
                ("review", models.IntegerField(default=0, null=True)),
                ("star", models.FloatField(blank=True, default=0, null=True)),
                ("image", models.CharField(blank=True, max_length=256, null=True)),
                ("agency", models.CharField(blank=True, max_length=256)),
                ("url", models.CharField(blank=True, max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Shop",
        ),
        migrations.RemoveField(
            model_name="product",
            name="shop",
        ),
        migrations.AddField(
            model_name="product",
            name="seller",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="crawler.seller",
            ),
        ),
    ]
