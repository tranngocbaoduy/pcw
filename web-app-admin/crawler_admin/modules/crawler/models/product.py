import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen, ExtractInfoIphone, ExtractInfoMacbook
from modules.crawler.models.sitemap import PageInfo
from pprint import pprint

class Category(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 
    name = models.CharField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '#C{} - {}'.format(self.id, self.name)
    
    class Meta:
        verbose_name = _('Category')
        ordering = ['name'] 

class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=256)
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)
    meta = models.JSONField(default=dict) 

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#GP{} - {}'.format(self.id, self.name)

    class Meta:
        verbose_name = _('Group Product')
        ordering = ['name'] 


class Product(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    base_url = models.CharField(max_length=512, default='')
    name = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    encoded_base_url = models.CharField(max_length=512) 
    price = models.FloatField(default=0, blank=True, null=True)
    list_price = models.FloatField(default=0, blank=True, null=True)
    discount_rate = models.IntegerField(default=0, blank=True, null=True)
    is_subscribe = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group_product = models.ForeignKey(GroupProduct, on_delete=models.CASCADE, blank=True, null=True)

    meta = models.JSONField(default=dict) 
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)

    count_update = models.IntegerField("Count Update", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#P{} - {}'.format(self.id, self.name)

    def get_base_url(self):
        return self.base_url
    
    class Meta:
        ordering = ['group_product__name']

    def categorize(self,): 
        base_url = self.base_url
        
        if self.category.name == 'Điện thoại':
            gen_number, storage_size, is_used = ExtractInfoIphone().extract_info(base_url) 
            if storage_size and gen_number and not is_used:
                pprint({
                    'gen_number': gen_number,
                    'storage_size': storage_size,
                    'url': base_url,   
                })
                obj, is_created = GroupProduct.objects.get_or_create(name='{}#{}'.format(gen_number,storage_size))
                obj.category = self.category
                obj.save()
                self.group_product = obj
                self.save()
        elif self.category.name == 'Macbook':
            extracted_info = ExtractInfoMacbook().extract_info(base_url, self.title) 
            if extracted_info['mac_type'] and extracted_info['screen_size'] and extracted_info['gen_number']:
                obj, is_created = GroupProduct.objects.get_or_create(name='MAC{}#{}#{}'.format(extracted_info['mac_type'],extracted_info['gen_number'],extracted_info['screen_size']))
                obj.category = self.category
                obj.save()
                self.group_product = obj
                self.save()
           
            
                # print('[data] =>',gen_number, '\t',storage_size, '\t', is_used,'\t',i) 

        # final_data = list(sorted(final_data, key=lambda x: (x['gen_number'], x['storage_size']), reverse=True))
        # for i in final_data: 
        #     if '{}#{}'.format(i['gen_number'], i['storage_size']) not in group:
        #         group['{}#{}'.format(i['gen_number'], i['storage_size'])] = []
        #     group['{}#{}'.format(i['gen_number'], i['storage_size'])].append(i['url'])
        #     print('{} \t\t- {} - {}'.format(i['gen_number'], i['storage_size'],i['url']))  

        # for key, value in group.items():
        #     print('{}'.format(key))
        #     pprint(value)
        
    def check_subscribe(self,):  
        try:
            page_info = PageInfo.objects.get(encoded_base_url=self.encoded_base_url)
            if page_info and page_info.is_subscribe != self.is_subscribe:
                self.is_subscribe = page_info['is_subscribe'] 
                self.save()
        except Exception as e:
            print('e', e)
 