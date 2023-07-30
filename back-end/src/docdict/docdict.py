import os
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

def update_dict(word_dict, seen, word, line_idx, start_index, end_index, sentence_idx):
    new_dict = {"line_idx": line_idx, "start": start_index, "end": end_index, "sentence_idx": sentence_idx}
    if word not in seen:
        word_dict[word] = [new_dict]
        seen.add(word)
    else:
        word_dict[word].append(new_dict)


def get_word_details(original_file):
    # it will store the start and end index of each line in the file, the index is [start, end)
    # it is used to find the index range of word
    lines_range = []
    # initialize line_range first
    with open(original_file, 'r') as file:
        before = 0

        lines = file.readlines()
        for line in lines:
            # [left, right)
            lines_range.append((before, before + len(line)))
            before += len(line)

    total_line = len(lines_range)

    # generate the word dict through retrieving sentences
    seen = set()
    word_dict = {}
    with open(original_file, 'r') as file:
        text = file.read()

        sentences = sent_tokenize(text)
        line_start = 0
        for sentence_idx, sentence in enumerate(sentences):
            sentence_start = text.find(sentence, line_start)
            sentence_end = sentence_start + len(sentence)
            check_start = sentence_start
            words_in_sentence = word_tokenize(sentence)
            for word in words_in_sentence:
                word_start = text.find(word, check_start)
                if word_start != -1:
                    word_end = word_start + len(word)
                    # update line_start
                    while word_end >= lines_range[line_start][1]:
                        line_start += 1

                    # add 1 as the index begins with 1 not from 0 (for line_index, start_index, end_index)
                    start_index = word_start - lines_range[line_start][0] + 1
                    end_index = word_end - lines_range[line_start][0] + 1
                    update_dict(word_dict, seen, word, line_start + 1, start_index, end_index, sentence_idx)

                    # update status
                    check_start = word_end
    return word_dict, sentences

def init_dict():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'doc')

    files = os.listdir(file_path)

    file_list = [f.split('.')[0] for f in files if os.path.isfile(os.path.join(file_path, f))]

    # file_dict_path = '../doc/docdicts'
    file_dict_path = os.path.join(base_dir, '..', 'doc/docdicts')

    for file_name in file_list:
        dict_file_path = os.path.join(file_dict_path, f'{file_name}_dict.txt')
        # sentences_ref_file_path = os.path.join(file_dict_path, f'{file_name}_sentence.txt')
        if not os.path.exists(dict_file_path):
            new_dict, sentences = get_word_details(os.path.join(file_path, f'{file_name}.txt'))
            with open(dict_file_path, 'w') as file:
                for key, value in new_dict.items():
                    json_obj = json.dumps({key: value})
                    file.write(json_obj + '\n')
            # with open(sentences_ref_file_path, 'w') as file:
            #     for sentence in sentences:
            #         file.write(sentence+'\n')