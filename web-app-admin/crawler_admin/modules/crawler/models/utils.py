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
    def extract_ram_size(url):
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
        ram_size = ExtractInfoIphone().extract_ram_size(base_url) 
        is_used = ExtractInfoIphone().extract_is_used(base_url)
        if ram_size and gen_number and not is_used:
            return gen_number, ram_size, is_used
        if gen_number and not is_used and ram_size == '' and name_sp != '':
            ram_size = ExtractInfoIphone().extract_ram_size(name_sp) 
            if ram_size and gen_number and not is_used:
                return gen_number, ram_size, is_used
        return None, None, None

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        gen_number, ram_size, _ = ExtractInfoIphone().extract_info(base_url, name_sp)
        if gen_number and ram_size:
            return True
        return False