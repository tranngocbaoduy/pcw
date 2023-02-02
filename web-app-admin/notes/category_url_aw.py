
import string
import random 
import re 
from pprint import pprint
# type: string
# gen_number: integer
# ram_size: integer
# storage_size: integer
# color: string

class ExtractInfoAppleWatch(object):

    @staticmethod
    def extract_gen_number(text):
        regexs = [
            ' (\d{4}) ',
            '-(\d{4})-', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-',' ').strip()
        return None

    @staticmethod
    def extract_gen_name(text):
        regexs = [ 
            '-s(\d{1})',
            '-series-(\d{1})',
            '-se',
            '-ultra',
            '-nike',
            's(\d{1})-',
            'series-(\d{1})-',
            'se-',
            'ultra-',
            'nike-',
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                name = match.group().replace('-',' ').strip()
                name = name.replace('series ','s')
                if 'watch-se' in name:
                    gen_number = ExtractInfoAppleWatch.extract_gen_number(text)
                    return f'{name}-{gen_number}'
                return name
        return None
     
    @staticmethod
    def extract_size_number(text):
        regexs = [
            '-(\d{2})mm-',
            ' (\d{2})mm ', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-',' ').strip()
        return None
    
    @staticmethod
    def extract_network_support(text):
        if ('gps' in text and 'cellular' in text) or 'lte' in text: return 'lte'
        if 'gps' in text: return 'gps'
        return None
    
    @staticmethod
    def extract_border(text):
        regexs = [
            '-vien-([a-z]{3,6})', 
            ' vien ([a-z]{3,6})', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-',' ').strip()
        return None


    @staticmethod
    def extract_is_used(text):
        regexs = [
            '-cu',  
            ' cũ ',
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return True
        return False

    @staticmethod
    def pre_extract(text):
        text = text.lower()    
        gen_name = ExtractInfoAppleWatch.extract_gen_name(text)
        size_number = ExtractInfoAppleWatch.extract_size_number(text) 
        border = ExtractInfoAppleWatch.extract_border(text) 
        network_support = ExtractInfoAppleWatch.extract_network_support(text) 
        is_used = ExtractInfoAppleWatch.extract_is_used(text) 
        return { 
            'gen_name': gen_name,  
            'size_number': size_number,
            'network_support': network_support,
            'border': border, 
            'is_used': is_used
        }

    @staticmethod
    def extract_info(base_url, name_sp=""):
        info_from_base_url = dict(ExtractInfoAppleWatch.pre_extract(base_url))
        info_from_name = dict(ExtractInfoAppleWatch.pre_extract(name_sp))
        for k, v in info_from_name.items(): 
            if v and info_from_base_url[k] == None and info_from_base_url[k] != v:
                info_from_base_url[k] = v
            if k == 'is_used':
                if v == True or info_from_base_url[k] == True:
                    info_from_base_url[k] = True
 
        return info_from_base_url

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        extracted_info = ExtractInfoAppleWatch.extract_info(base_url, name_sp)
        if ExtractInfoAppleWatch.is_candidate_item(extracted_info):
            return True
        return False
    
    @staticmethod
    def is_candidate_item(extracted_info):  
        if extracted_info['gen_name']:
            return True
        return False

with open('./notes/data_topzone_aw.txt', 'r') as f:
    data = f.read()
    data = data.split('\n')

final_data = []
print(len(data))

for i in data: 
    url, name_sp = i.split('\t')
    extracted_info = ExtractInfoAppleWatch.extract_info(url, name_sp) 
    if ExtractInfoAppleWatch.is_candidate_item(extracted_info):
        final_data.append(extracted_info)
    # else:
    print('=>',i)
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
    