# Generated by Django 3.2.15 on 2023-01-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0013_alter_product_group_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='count_update',
            field=models.IntegerField(default=1, verbose_name='Count Update'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=512),
        ),
    ]