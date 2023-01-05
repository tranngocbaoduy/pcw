# Generated by Django 3.2.15 on 2023-01-05 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_sitemap_exclude_search_terms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageinfo',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='scraper',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='scrapersitemap',
            options={'ordering': ['sitemap']},
        ),
        migrations.AlterModelOptions(
            name='sitemap',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='sitemap',
            name='ware_parser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crawler.wareparser'),
        ),
        migrations.AlterField(
            model_name='sitemap',
            name='exclude_search_terms',
            field=models.CharField(blank=True, default='dat-truoc,su-kien,event,quay-,tai-nghe,&,filter,loc,so-sanh,san-pham-moi,cong-nghe,nguoi-,khuyen-mai,phu-kien,combo,tag,dchannel,tragop,zalo,tra-gop,news,tekzone,the-,hub-,cap-,cuong-luc,bao-,mieng-,sac-,op-,mua-', max_length=512),
        ),
        migrations.AlterField(
            model_name='sitemap',
            name='limit_page',
            field=models.CharField(default='500', max_length=256),
        ),
        migrations.AlterField(
            model_name='sitemap',
            name='target_search_terms',
            field=models.CharField(blank=True, default='apple-iphone-,iphone-14,iphone-13,iphone-12,iphone-11,iphone-se', max_length=512),
        ),
    ]
