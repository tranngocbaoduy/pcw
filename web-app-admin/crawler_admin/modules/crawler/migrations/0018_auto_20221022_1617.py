# Generated by Django 3.2.15 on 2022-10-22 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0017_auto_20221022_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spider',
            name='parser_wait_until_child',
        ),
        migrations.AlterField(
            model_name='spider',
            name='parser_wait_until_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crawler.parserwaituntil'),
        ),
    ]