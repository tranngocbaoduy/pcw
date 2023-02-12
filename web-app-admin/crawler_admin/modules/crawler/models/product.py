import uuid
import json

from urllib.parse import urlparse
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen, ExtractInfoIphone, ExtractInfoMacbook, ExtractInfoAppleWatch
from modules.crawler.models.sitemap import PageInfo
from pprint import pprint
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


def get_domain(url): 
    # print('url:', url.base_url)
    o = urlparse(url)
    return str(o.netloc) 


class Category(MPTTModel): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 
    name = models.CharField(max_length=256) 
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, db_index=True, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '#C{} - {}'.format(self.id, self.name)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name'] 

    class MPTTMeta:
        order_insertion_by = ['name']
     

class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=256,db_index=True,)
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)
    meta = models.JSONField(default=dict) 

    store_name = models.CharField(max_length=512, db_index=True,blank=True, default="")
    largest_price = models.FloatField(default=0, db_index=True,blank=True, null=True)
    smallest_price = models.FloatField(default=0, db_index=True,blank=True, null=True)
    category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#GP{} - {}'.format(self.id, self.name)

    def remove_group_has_0_subscribers(self):
        count_product = len(Product.objects.filter(group_product=self.id))     
        if count_product == 0:
            self.delete()

    def update_info_detail(self):
        product_items = Product.objects.filter(group_product=self.id)
        description = []
        meta = []
        price = []
        list_image = []
        store_name = []

        for product in product_items:
            if product.price and product.price > 0: price.append(product.price)
            if product.description: description.append(product.description)
            if product.meta: meta.append(product.meta)
            if product.list_image: list_image.append(product.list_image)

            domain = get_domain(product.base_url)
            if domain not in store_name:
                store_name.append(domain)
        

        self.description = list(sorted(description, key=lambda x: len(x), reverse=True))
        self.meta = list(sorted(meta, key=lambda x: len(x), reverse=True))
        self.list_image = list(sorted(list_image, key=lambda x: len(x), reverse=True))
        price = list(sorted(price, key=lambda x: x, reverse=True))
        self.largest_price = price[0]
        self.smallest_price = price[-1]

        # self.description = self.description[0] if self.description != [] else ''
        self.meta = self.meta[0] if self.meta != [] else ''
        self.list_image = self.list_image[0] if self.list_image != [] else ''
        self.store_name = ','.join(store_name)

        self.save()
        
    @staticmethod
    def update_all_info():
        groups = GroupProduct.objects.all()
        for group in groups:
            group.update_info_detail()
            group.remove_group_has_0_subscribers()

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
    price = models.FloatField(default=0,db_index=True, blank=True, null=True)
    list_price = models.FloatField(default=0,db_index=True, blank=True, null=True)
    discount_rate = models.IntegerField(default=0,db_index=True, blank=True, null=True)
    is_subscribe = models.BooleanField(default=True,db_index=True,)
    is_used = models.BooleanField(default=False,db_index=True,)
    last_updated_price = models.DateTimeField(auto_now_add=True,db_index=True,)

    category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE)
    group_product = models.ForeignKey(GroupProduct, db_index=True, on_delete=models.CASCADE, blank=True, null=True)

    meta = models.JSONField(default=dict) 
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)

    count_update = models.IntegerField("Count Update", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Product #{}'.format(self.id)

    def get_base_url(self):
        return self.base_url
    
    def tags(self):
        return self.group_product and self.group_product.name.split('#') if self.group_product else []
    
    class Meta:
        ordering = ['group_product__name']

    def categorize(self,): 
        base_url = self.base_url 
        if self.category.name == 'iPhone':
            extracted_info = ExtractInfoIphone.extract_info(base_url, self.title) 
            pprint(extracted_info) 
            if ExtractInfoIphone.is_candidate_item(extracted_info): 
                obj, is_created = GroupProduct.objects.get_or_create(name='{}#{}#'.format(extracted_info['gen_number'],extracted_info['storage_size']))
                obj.category = self.category
                obj.save()
                self.group_product = obj 
                self.is_subscribe = True
            else:
                self.group_product = None
                self.is_subscribe = False 
            meta = json.loads(self.meta) 
            meta.update(extracted_info)
            self.meta = json.dumps(meta)
            self.is_used = extracted_info.get('is_used', False)
            self.save()
        elif self.category.name == 'Macbook':
            extracted_info = ExtractInfoMacbook.extract_info(base_url, self.title) 
            pprint(extracted_info)
            if ExtractInfoMacbook.is_candidate_item(extracted_info):
                obj, is_created = GroupProduct.objects.get_or_create(name='MACBOOK_{}#{}#{}#{}#{}#{}#{}#'.format(
                    extracted_info.get('mac_type').upper() if extracted_info.get('mac_type') else 'UNKNOW',
                    extracted_info.get('gen_number').upper() if extracted_info.get('gen_number') else 'UNKNOW',
                    extracted_info.get('gen_name').upper() if extracted_info.get('gen_name') else 'UNKNOW',
                    extracted_info.get('screen_size').upper() if extracted_info.get('screen_size') else 'UNKNOW',
                    extracted_info.get('storage_size').upper() if extracted_info.get('storage_size') else 'UNKNOW',
                    extracted_info.get('ram_size').upper() if extracted_info.get('ram_size') else 'UNKNOW',
                    extracted_info.get('core_number').upper() if extracted_info.get('core_number') else 'UNKNOW',))
                obj.category = self.category
                obj.save()
                self.group_product = obj
                self.is_subscribe = True
            else:
                self.group_product = None
                self.is_subscribe = False 
            meta = json.loads(self.meta) 
            meta.update(extracted_info)
            self.meta = json.dumps(meta)
            self.is_used = extracted_info.get('is_used', False)
            self.save()

        elif self.category.name == 'Apple Watch':
            extracted_info = ExtractInfoAppleWatch.extract_info(base_url, self.title) 
            pprint(extracted_info)
            if ExtractInfoAppleWatch.is_candidate_item(extracted_info):
                obj, is_created = GroupProduct.objects.get_or_create(name='APPLE_WATCH_{}#{}#{}#{}#'.format(
                    extracted_info.get('gen_name').upper() if extracted_info.get('gen_name') else 'UNKNOW',
                    extracted_info.get('size_number').upper() if extracted_info.get('size_number') else 'UNKNOW',
                    extracted_info.get('network_support').upper() if extracted_info.get('network_support') else 'UNKNOW',
                    extracted_info.get('border').upper() if extracted_info.get('border') else 'UNKNOW',))
                obj.category = self.category
                obj.save()
                self.group_product = obj 
                self.is_subscribe = True
            else:
                self.group_product = None
                self.is_subscribe = False 
            meta = json.loads(self.meta) 
            meta.update(extracted_info)
            self.meta = json.dumps(meta)
            self.is_used = extracted_info.get('is_used', False)
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
    
    def update_discount_rate(self):
        p1 = Decimal(self.price)
        p2 = Decimal(self.list_price)
        if p1 and p1 > 0 and p2 and p2  > 0:
            if p1 * 2 < p2:
                self.list_price = p1
                p2 = p1
                discount_rate = 0
            else:
                discount_rate = 100 - int(Decimal(p1) / Decimal(p2) * 100)
        self.discount_rate = discount_rate     
        self.save()

    def check_subscribe(self,):  
        try:
            page_info = PageInfo.objects.get(encoded_base_url=self.encoded_base_url)
            if page_info:
                is_candidate = False
                if self.category.name == 'iPhone' and ExtractInfoIphone.is_candidate_url(self.base_url, self.title):
                    is_candidate = True
                elif self.category.name == 'Macbook' and ExtractInfoMacbook.is_candidate_url(self.base_url, self.title):
                    is_candidate = True
                if is_candidate:
                    if page_info.is_subscribe != self.is_subscribe:
                        self.is_subscribe = page_info.is_subscribe 
                else:
                    self.is_subscribe = False
                    page_info.is_subscribe = False
                    page_info.save()
                self.update_discount_rate()
                self.save()
        except ObjectDoesNotExist as e:
            self.delete()

        except Exception as e:
            print('e', e.code)
    
    @staticmethod
    def categorize_all():
        list_product = Product.objects.all()
        for product in list_product:
            product.update_discount_rate()
            product.categorize()

class HistoryPricing(models.Model):
    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    price = models.FloatField(default=0, blank=True, null=True)
    list_price = models.FloatField(default=0, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '#History {} belongs to {}'.format(self.id, self.product.id)
