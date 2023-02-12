# Generated by Django 4.1.3 on 2023-02-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0034_groupproduct_largest_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount_rate",
            field=models.IntegerField(blank=True, db_index=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="is_subscribe",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="is_used",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name="product",
            name="last_updated_price",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="list_price",
            field=models.FloatField(blank=True, db_index=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(blank=True, db_index=True, default=0, null=True),
        ),
    ]
