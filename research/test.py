from pyvi import ViTokenizer, ViPosTagger

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')

def main():

    dictionary_filename = 'dictionary.txt'
    dictionary = read_file(dictionary_filename)
    brand = 'samsung'
    data = read_file('data_name_phone.txt')
    save_data= []
    for i in data:
        i = i.replace('\n', '')
        i = ' '.join(i.split())
        print(' '.join(i.split()))
        sents, postagging = ViPosTagger.postagging(ViTokenizer.tokenize(u"{}".format(i)))
        keep_words = [brand]
        for index, pos in enumerate(postagging):
            tags = sents[index].split('_')
            flag = True
            for m in tags:
                if m in dictionary:
                    flag = False
            if (pos == 'N' or pos == 'V') and flag and sents[index] and sents[index] != '' and sents[index] not in keep_words: 
                keep_words.append(sents[index])
        if len(keep_words) != 1: print(keep_words, '==', i, postagging)
        save_data.append(" ".join(keep_words))
    with open('output.txt', 'w') as f:
        for k in save_data:
            f.write(k+'\n')
if __name__ == '__main__':
    main()