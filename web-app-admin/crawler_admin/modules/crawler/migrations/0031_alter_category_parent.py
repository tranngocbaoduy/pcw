# Generated by Django 4.1.3 on 2023-01-29 09:01

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0030_rename_parent_category_category_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parent_category",
                to="crawler.category",
            ),
        ),
    ]
