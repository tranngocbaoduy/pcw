import numpy as np
import regex as re

from fuzzywuzzy import fuzz
from pyvi import ViTokenizer, ViPosTagger
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

class NLPCategory2Code():
    
    def __init__(self, id_cate, corpus, corpus_url=[],threshold=0.3):
        self.id_cate = id_cate
        self.init_corpus= corpus
        self.corpus= corpus
        self.corpus_url = corpus_url
        self.sent2code = {}
        self.code2sent = {}
        self.threshold=threshold
        self.model = None
        self.X = None

        self.code2SK = {}
        self.SK2code = {} 

        
    def get_corpus(self):
        """
            get corpus
        """
        return self.corpus
        
    def pre_handel(self):
        """
            tokenize word and clean word before training
        """
        new_corpus = []
        for sentence in self.corpus:
            is_skip_next_word = False
            new_sentence = []
            sentence = ViTokenizer.tokenize(sentence)
            for word in sentence.split(' '):
#                 if is_number(word):
#                     new_sentence.append(word)
#                     is_skip_next_word = True
#                     continue
#                 if is_skip_next_word: 
#                     new_sentence[-1] += word
#                     is_skip_next_word = False
#                 else: 
                new_sentence.append(word.replace('ml',''))
            
            new_corpus.append(" ".join(new_sentence))
        self.corpus = new_corpus.copy()
        
    def fit(self):
        """
            find weight of word in corpus
        """
        name_model = self.id_cate
        self.model = TfidfVectorizer(
            analyzer='word', 
            sublinear_tf=True,
            strip_accents='unicode',
            token_pattern=r'\w{1,}', 
            stop_words=None)
        self.X = self.model.fit_transform(self.corpus) 

    def get_index_word(self, word):
        """
            get index of word in feature name
        """
        return self.model.get_feature_names().index(word) if self.model != None else None
    
    def map_weight_to_sentence(self):
        """
            get weight matrix of corpus
        """
        list_weight_of_sentence = []
        for index, sentence in enumerate(self.corpus):
            sentence = sentence.lower()
            weight_of_sentence = []
            for word in sentence.split(' '): 
                try: 
                    word_index_model = self.get_index_word(word) 
                    weight_of_sentence.append(self.X[index,word_index_model]) 
                except: 
                    weight_of_sentence.append(0)
            list_weight_of_sentence.append(weight_of_sentence)
        self.weight_corpus = list_weight_of_sentence.copy()
        return list_weight_of_sentence
    

    def get_weight(self, sentence):
        """
            filter word by threshold, if weight smaller threshold, it'll be remove
        """  
        word_tokens = sentence.split(' ')
        index = self.corpus.index(sentence)
        weight_tokens = self.weight_corpus[index]
        filtered_sentence = []
        for i, word in enumerate(word_tokens):
            if weight_tokens[i] < self.threshold and weight_tokens[i] > 0:
                continue
            else:
                filtered_sentence.append(word)
        return " ".join(filtered_sentence)
    
    def filter_corpus(self):
        """
            filter word by threshold, if weight smaller threshold, it'll be remove
        """
        self.filtered_corpus = []

        for index, sentence in enumerate(self.corpus):
            self.filtered_corpus.append(self.get_weight(sentence))
        return self.filtered_corpus
    
    def get_longest_sentence(self, sents):
        map_item = list(map(lambda x: len(x), sents))
        max_item = max(map_item)
        return sents[map_item.index(max_item)]
    
    def get_code_by(self, corpus):
        """
            filter word by code product, if word contain both letter and number => it's code product (ID)
        """
#         rx = re.compile(r'(?=.*[a-zA-Z])(?=.*[@#\d])[a-zA-Z\d]{3,}')
        rx = re.compile(r'(?:\d+[a-zA-Z]+|[a-zA-Z]+\d+)')
        rx_longest = re.compile(r'([\w\/\-\_]+)')
        SENT_2_CODE = [] 
        SENT_2_CODE_LONGEST_WORD = []
        for sentence in (corpus):   
            filtered_sentence = rx.findall(sentence)
            filtered_longest_sentence = rx_longest.findall(sentence)
            if len(filtered_sentence) == 0:
                SENT_2_CODE.append("")
            else:
                SENT_2_CODE.append(" ".join(filtered_sentence))
            if len(filtered_longest_sentence) == 0:
                SENT_2_CODE_LONGEST_WORD.append("")
            else:
                SENT_2_CODE_LONGEST_WORD.append(self.get_longest_sentence(filtered_longest_sentence)) 
        return SENT_2_CODE, SENT_2_CODE_LONGEST_WORD
     
    
    def build(self):
        """
            build model from corpus to code product
        """
        self.pre_handel()
        self.fit()  
        self.map_weight_to_sentence()
        
        self.CODE_FROM_INIT_SENTENCE, self.CODE_LONGEST_FROM_INIT_SENTENCE = self.get_code_by(self.init_corpus) 
        self.CODE_FROM_FILTER_SENTENCE, self.CODE_LONGEST_FROM_FILTER_SENTENCE = self.get_code_by(self.filter_corpus()) 
        self.CODE_FROM_URL, self.CODE_LONGEST_FROM_URL = self.get_code_by(self.corpus_url)
         
    def get_code_of_sentence(self, sent):
        index = self.init_corpus.index(sent)
        return {
            "by_init":self.CODE_FROM_INIT_SENTENCE[index].replace(' ',''), 
            "by_name":self.CODE_FROM_FILTER_SENTENCE[index].replace(' ',''),
            "by_url":self.CODE_FROM_URL[index].replace(' ','').replace('com/','')
        }
    
    def get_code_longest_of_sentence(self, sent):
        index = self.init_corpus.index(sent)
        return {
            "by_init":self.CODE_LONGEST_FROM_INIT_SENTENCE[index].replace(' ',''), 
            "by_name":self.CODE_LONGEST_FROM_FILTER_SENTENCE[index].replace(' ',''),
            "by_url":self.CODE_LONGEST_FROM_URL[index].replace(' ','').replace('com/','')
        }