import uuid
import string
import random 
import re 

def id_generator(size=12):
    chars= string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def id_gen(ID_LENGTH=10) -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return str(uuid.uuid4().int)[:ID_LENGTH]


class ExtractInfoIphone(object):

    @staticmethod
    def extract_gen_number(text):
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
            match = re.search(regex, text)
            if match:
                return '_'.join(match.group().split('-')).upper()
        return ''

    @staticmethod
    def extract_storage_size(text):
        regexs = [
            '(\d+)tb', 
            '(\d+)gb', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().upper()
        return ''


    @staticmethod
    def extract_is_used(text):
        regexs = [
            '-cu',  
            ' cũ ', 
            ' 99% ',
            ' 99',
            'tray-xuoc',
            'like',
            'trầy'
        ] 
        for regex in regexs:
            match = re.search(regex, text) 
            if match:
                for i in ['thu cũ', 'thu-cu']:
                    if i in text:
                        return False 
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
        extracted_info = ExtractInfoIphone.extract_info(base_url.lower(), name_sp.lower())
        if ExtractInfoIphone.is_candidate_item(extracted_info):
            return True
        return False
    
    @staticmethod
    def is_candidate_item(extracted_info):  
        if extracted_info['storage_size'] and extracted_info['gen_number']:
            return True
        return False 

class ExtractInfoMacbook(object):

    @staticmethod
    def extract_type(text):
        regexs = [
            '-pro-',
            ' pro ',
            '-air-', 
            ' air ', 
            'imac-', 
            'imac ', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-','').strip()
        return None

    @staticmethod
    def extract_gen_number(text):
        regexs = [
            ' (\d{4}) ',
            '-(\d{4})-', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-','').strip()
        return None
    
    @staticmethod
    def extract_gen_name(text):
        regexs = [
            'm1',
            'm2', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-','').strip()
        return None
    
    @staticmethod
    def extract_screen_size_number(text):
        regexs = [
            '-(\d{2})-',
            ' (\d{2}) ', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                res = match.group().replace('-','').strip()
                if res in ['10']: return None
                return f'{res}inch'
        return None
    
    @staticmethod
    def extract_core_number(text):
        regexs = [
            ' (\d{2}) core', 
            ' (\d{2})-core',
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                res = match.group().replace('-','').strip()
                if res in ['10']: return None
                return res.replace(' core','-core')
        return None

    @staticmethod
    def extract_ram_size(text):
        regexs = [
            '(\d{1,2})gb', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group()
        return None
        
    
    @staticmethod
    def extract_storage_size(text):
        regexs = [
            '(\d{3})gb', 
            '(\d+)tb', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().strip()
        return None


    @staticmethod
    def extract_is_used(text):
        regexs = [
            '-cu',  
            ' cũ ', 
            ' 99% ',
            ' 99',
            'tray-xuoc',
            'like',
            'da-kich-hoat',
            'đã kích hoạt',
            'trầy'
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                for i in ['thu cũ', 'thu-cu']:
                    if i in text:
                        return False 
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
        core_number = ExtractInfoMacbook.extract_core_number(text) 
        is_used = ExtractInfoMacbook.extract_is_used(text) 
        return {
            'mac_type': mac_type, 
            'screen_size': screen_size, 
            'gen_name': gen_name, 
            'gen_number': gen_number, 
            'ram_size': ram_size, 
            'storage_size': storage_size, 
            'core_number': core_number,
            'is_used': is_used
        }

    @staticmethod
    def extract_info(base_url, name_sp=""):
        info_from_base_url = dict(ExtractInfoMacbook.pre_extract(base_url))
        info_from_name = dict(ExtractInfoMacbook.pre_extract(name_sp)) 
         
        for k, v in info_from_name.items(): 
            if v and info_from_base_url[k] == None and info_from_base_url[k] != v:
                info_from_base_url[k] = v
            if k == 'is_used':
                if v == True or info_from_base_url[k] == True:
                    info_from_base_url[k] = True
            if k == 'gen_name' and info_from_base_url[k] == None:
                info_from_base_url[k] = 'normal'
 
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
        return 'gps'
    
    @staticmethod
    def extract_border(text):
        regexs = [
            '-vien-([a-z]{3,6})', 
            ' vien ([a-z]{3,6})', 
        ] 
        for regex in regexs:
            match = re.search(regex, text)
            if match:
                return match.group().replace('-',' ').strip().replace(' ','_')
        return None

    @staticmethod
    def extract_is_used(text):
        regexs = [
            '-cu',  
            ' cũ ', 
            ' 99% ',
            ' 99',
            'tray-xuoc',
            'like',
            'trầy'
        ] 
        for regex in regexs:
            match = re.search(regex, text) 
            if match:
                for i in ['thu cũ', 'thu-cu']:
                    if i in text:
                        return False 
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