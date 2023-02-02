
import string
import random 
import re 
from pprint import pprint
# type: string
# gen_number: integer
# ram_size: integer
# storage_size: integer
# color: string

class ExtractInfoMacbook(object):

    @staticmethod
    def extract_type(url):
        regexs = [
            '-pro-',
            ' pro ',
            '-air-', 
            ' air ', 
            'imac-', 
            'imac ', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().replace('-','').strip()
        return None

    @staticmethod
    def extract_gen_number(url):
        regexs = [
            ' (\d{4}) ',
            '-(\d{4})-', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().strip()
        return None
    
    @staticmethod
    def extract_gen_name(url):
        regexs = [
            'm1',
            'm2', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().strip()
        return ''
    
    @staticmethod
    def extract_screen_size_number(url):
        regexs = [
            '-(\d{2})-',
            ' (\d{2}) ', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().replace('-','').strip()
        return None

    @staticmethod
    def extract_ram_size(url):
        regexs = [
            '(\d{1,2})gb', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group()
        return None
        
    
    @staticmethod
    def extract_storage_size(url):
        regexs = [
            '(\d{3})gb', 
            '(\d+)tb', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group().strip()
        return None


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
        mac_type = ExtractInfoMacbook.extract_type(text)
        screen_size = ExtractInfoMacbook.extract_screen_size_number(text)
        gen_number = ExtractInfoMacbook.extract_gen_number(text)
        gen_name = ExtractInfoMacbook.extract_gen_name(text)
        storage_size = ExtractInfoMacbook.extract_storage_size(text) 
        ram_size = ExtractInfoMacbook.extract_ram_size(text) 
        is_used = ExtractInfoMacbook.extract_is_used(text) 
        return {
            'mac_type': mac_type, 
            'screen_size': screen_size, 
            'gen_name': gen_name, 
            'gen_number': gen_number, 
            'ram_size': ram_size, 
            'storage_size': storage_size, 
            'is_used': is_used
        }

    @staticmethod
    def extract_info(base_url, name_sp=""):
        info_from_base_url = dict(ExtractInfoMacbook.pre_extract(base_url))
        info_from_name = dict(ExtractInfoMacbook.pre_extract(name_sp))
        
        print("\n==")
        print(info_from_base_url)
        print('\n=\n')
        print(info_from_name)
        print("==\n")

        for k, v in info_from_name.items(): 
            if v and info_from_base_url[k] == None and info_from_base_url[k] != v:
                info_from_base_url[k] = v
            if k == 'is_used':
                if v == True or info_from_base_url[k] == True:
                    info_from_base_url[k] = True
 
        return info_from_base_url

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        extracted_info = ExtractInfoMacbook.extract_info(base_url, name_sp)
        if ExtractInfoMacbook.is_candidate_item(extracted_info):
            return True
        return False
    
    @staticmethod
    def is_candidate_item(extracted_info):  
        if extracted_info['mac_type'] and extracted_info['screen_size'] and extracted_info['gen_number']:
            return True
        return False

with open('./notes/data.txt', 'r') as f:
    data = f.read()
    data = data.split('\n')

final_data = []
print(len(data))

for i in data:
    print(i)
    url, name_sp = i.split('\t')
    extracted_info = ExtractInfoMacbook.extract_info(url, name_sp) 
    
    if ExtractInfoMacbook.is_candidate_item(extracted_info):
        final_data.append(extracted_info)
    else:
        print(i)
        print(extracted_info)
        print()
        print()
        # print('[data] =>',gen_number, '\t',ram_size, '\t', is_used,'\t',i) 

group = {}
# final_data = list(sorted(final_data, key=lambda x: (x['gen'], x['ram_size']), reverse=True))
# for i in final_data: 
#     if '{}#{}'.format(i['gen_number'], i['ram_size']) not in group:
#         group['{}#{}'.format(i['gen_number'], i['ram_size'])] = []
#     group['{}#{}'.format(i['gen_number'], i['ram_size'])].append(i['url'])
#     print('{} \t\t- {} - {}'.format(i['gen_number'], i['ram_size'],i['url']))  
print("--------------------------------\n\n")
print(len(final_data))
# for value in final_data: 
#     print(value)
    