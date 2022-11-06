# importing csv module
import csv
import re

def read_csv(filename):
 
    # initializing the titles and rows list
    fields = []
    rows = []
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        for row in csvreader:
            item = {}
            for index, val_col in enumerate(row):
                item[fields[index]] = val_col
            rows.append(item)
    
        # get total number of rows
        print("Total no. of rows: %d"%(csvreader.line_num))
    
    # printing the field names
    print('Field names are:' + ', '.join(field for field in fields))
    return fields, rows

def clean_word(str_content):
    str_content = str_content.lower()
    str_content = re.sub('/[^a-z0-9A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễếệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+/u', '', str_content)
    str_content = re.sub(r'[^\w\s]',' ', str_content)
    # str_content = re.sub(r'[0-9]+', ' ', str_content)
    str_content = str_content.replace('\n', ' ')
    str_content = str_content.replace('\t', ' ')
    str_content = re.sub("\s\s+", " ", str_content) 
    return str_content

def write_dict_txt(data):
    with open('dictionary.txt', 'w') as f:
        for item in data:
            # write each item on a new line
            f.write("%s\n" % item) 

def is_vietnamese(init_text): 
    text = re.sub('[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễếệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]', '', init_text)
    if init_text != text: return True
    return False

def remove_not_is_vietnamese(init_sentence): 
    words = init_sentence.split()
    new_sentence = [] 
    for word in words:
        if is_vietnamese(word): new_sentence.append(word)
    return " ".join(new_sentence)

def create_file_dictionary(): 
    # csv file name
    filename = "corpus-title-vn.txt"
    rows = read_file(filename).split('\n')
    print('len', len(rows))
    # fields, rows = read_csv(filename) 
    # rows = rows[:100000]
    content_rows = list(map(lambda x: remove_not_is_vietnamese(clean_word(x)), rows))

    str_content_rows = ' '.join(content_rows) 
    word_dict = list(set(str_content_rows.split())) 
    word_dict = list(filter(lambda word:  len(word) >= 2 and len(word) <= 7 and not word.isnumeric(), word_dict))
    word_dict = list(sorted(word_dict, key=lambda x: x, reverse=False)) 
    print('word_dict', len(word_dict))
    write_dict_txt(word_dict)

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def clean_name(name, dictionary):
    list_word = name.split()
    list_keep_word = []
    for word in list_word:
        if word not in dictionary:
            list_keep_word.append(word)
    return ' '.join(list_keep_word)

def check():
    filename = 'data_name.txt'
    data = read_file(filename).split('\n')

    dictionary_filename = 'dictionary.txt'
    dictionary = read_file(dictionary_filename).split('\n')
    
    for i in data[:1]: 
        convert_str = clean_name(clean_word(i), dictionary)
        print('[CHANGE] =>',convert_str,' \t\t ', i)
    
def main():
    create_file_dictionary()
    # check()
    # init_text = 'xả trạm bot cần thơ phụng hiệp cổ vũ đội tuyển u23 việt nam'
    # text = re.sub('[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễếệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]', '', init_text)
    # print('text', text)
    # print('init_text', init_text)

if __name__ == '__main__':
    main()