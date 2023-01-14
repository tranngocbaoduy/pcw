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
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return True
        return False
    
    @staticmethod
    def extract_info(base_url, name_sp=""):
        base_url = base_url.lower()
        name_sp = name_sp.lower()
        gen_number = ExtractInfoIphone().extract_gen_number(base_url)
        storage_size = ExtractInfoIphone().extract_storage_size(base_url) 
        is_used = ExtractInfoIphone().extract_is_used(base_url)
        if storage_size and gen_number and not is_used:
            return gen_number, storage_size, is_used
        if gen_number and not is_used and storage_size == '' and name_sp != '':
            storage_size = ExtractInfoIphone().extract_storage_size(name_sp) 
            if storage_size and gen_number and not is_used:
                return gen_number, storage_size, is_used
        return None, None, None

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        gen_number, storage_size, _ = ExtractInfoIphone().extract_info(base_url, name_sp)
        if gen_number and storage_size:
            return True 
        return False


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
        
        for k, v in info_from_name.items():
            if v and info_from_base_url[k] == None and info_from_base_url[k] != v:
                info_from_base_url[k] = v
 
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
 