
import string
import random 
import re 
from pprint import pprint
# type: string
# gen_number: integer
# ram_size: integer
# storage_size: integer
# color: string

class ExtractInfoIphone(object):

    @staticmethod
    def extract_gen_number(url):
        regexs = [
            'iphone-(\d+)-pro-max',
            'iphone-(\d+)-pro',
            'iphone-(\d+)-mini',
            'iphone-se',
            'iphone-se(-\d+)',
            'iphone-(\d+)-plus',
            'iphone-(\d+)'
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return '_'.join(match.group().split('-')).upper()
        return ''

    @staticmethod
    def extract_storage_size(url):
        regexs = [
            '(\d+)tb', 
            '(\d+)gb', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().upper()
        return ''


    @staticmethod
    def extract_is_used(url):
        regexs = [
            '-cu',  
            ' cũ ',
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return True
        return False
    
    @staticmethod
    def pre_extract(text):
        text = text.lower()   
        gen_number = ExtractInfoIphone().extract_gen_number(text)
        storage_size = ExtractInfoIphone().extract_storage_size(text) 
        is_used = ExtractInfoIphone().extract_is_used(text)
        return { 
            'gen_number': gen_number,  
            'storage_size': storage_size, 
            'is_used': is_used
        }

    @staticmethod
    def extract_info(base_url, name_sp=""):
        info_from_base_url = dict(ExtractInfoIphone.pre_extract(base_url))
        info_from_name = dict(ExtractInfoIphone.pre_extract(name_sp)) 
         
        for k, v in info_from_name.items(): 
            if v and info_from_base_url[k] == None and info_from_base_url[k] != v:
                info_from_base_url[k] = v
            if k == 'is_used':
                if v == True or info_from_base_url[k] == True:
                    info_from_base_url[k] = True
 
        return info_from_base_url

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        extracted_info = ExtractInfoIphone.extract_info(base_url, name_sp)
        if ExtractInfoIphone.is_candidate_item(extracted_info):
            return True
        return False
    
    @staticmethod
    def is_candidate_item(extracted_info):  
        if extracted_info['storage_size'] and extracted_info['gen_number'] and not extracted_info['is_used']:
            return True
        return False 

with open('./notes/data.txt', 'r') as f:
    data = f.read()
    data = data.split('\n')

final_data = []

for i in data:
    url, name_sp = i.split('\t')
    gen_number, ram_size, is_used = ExtractInfoIphone().extract_info(url, name_sp) 
    if ram_size and gen_number and not is_used:
        final_data.append({
            'gen_number': gen_number,
            'ram_size': ram_size,
            'url': i,            
        })
    else:
        print(i)
        # print('[data] =>',gen_number, '\t',ram_size, '\t', is_used,'\t',i) 

group = {}
final_data = list(sorted(final_data, key=lambda x: (x['gen_number'], x['ram_size']), reverse=True))
# for i in final_data: 
#     if '{}#{}'.format(i['gen_number'], i['ram_size']) not in group:
#         group['{}#{}'.format(i['gen_number'], i['ram_size'])] = []
#     group['{}#{}'.format(i['gen_number'], i['ram_size'])].append(i['url'])
#     print('{} \t\t- {} - {}'.format(i['gen_number'], i['ram_size'],i['url']))  

print(len(final_data))
# for key, value in group.items():
#     print('{}'.format(key))
#     pprint(value)
    