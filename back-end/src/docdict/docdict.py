import os
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import deque
from .trietree import Trie

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
            # init dict file for the document
            new_dict, sentences = get_word_details(os.path.join(file_path, f'{file_name}.txt'))
            with open(dict_file_path, 'w') as file:
                for key, value in new_dict.items():
                    json_obj = json.dumps({key: value})
                    file.write(json_obj + '\n')
            # init trie tree for the document
            # TODO: implement save_to_file_bfs() and load_from_file_bfs() in trietree 
            # and call the save method here

def _load_dict(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_dict_path = os.path.join(base_dir, '..', 'doc/docdicts')
    dict_file_path = os.path.join(file_dict_path, f'{filename}_dict.txt')

    with open(dict_file_path, 'r') as file:
        lines = file.readlines()

    loaded_dict = {}

    # parse the dictionary of the original file
    for line in lines:
        json_obj = json.loads(line)
        key, value = list(json_obj.items())[0]
        loaded_dict[key] = value
    return loaded_dict

def _read_sentences(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'doc', f'{filename}.txt')

    with open(file_path, 'r') as file:
        text = file.read()
        sentences = sent_tokenize(text)

    return sentences

def build_search_result_info(sentences, line_idx, start_idx, end_idx, sentence_idx):
    new_dict = {}
    new_dict["line"] = line_idx
    new_dict["start"] = start_idx
    new_dict["end"] = end_idx
    new_dict["in_sentence"] = sentences[sentence_idx]
    return new_dict

def generalSearchText(filename, word_in_search):
    word_dict = _load_dict(filename)
    print("successfully load word_dict", len(word_dict))
    sentences = _read_sentences(filename)
    print("successfully load sentences", len(sentences))
    word_sentence_set_list = []
    word_infos = []
    # TODO: change it and make the last word work as a prefix later
    noMatch = False
    keys = word_dict.keys()
    for word in word_in_search:
        if word not in keys:
            noMatch = True
            break
        else:
            word_info = word_dict[word]
            word_infos.append(word_info)
            word_sentence_idx = [info['sentence_idx'] for info in word_info]
            word_sentence_set_list.append(set(word_sentence_idx))
    if not noMatch:
        # check if the words are in the same sentence
        ref = word_sentence_set_list[0]
        for i in range(1, len(word_sentence_set_list)):
            ref = ref & word_sentence_set_list[i]
        noMatch = (len(ref)==0)
    if noMatch:
        return []
    # if match exists
    word_sentence_set_list = ref
    occurencies = []
    for sentence_idx in word_sentence_set_list:
        # TODO: fix later - current version it might facing issue in the case Now,...is..Now is...., when searching Now is
        # maybe use deque and check it based on the index of the first word and last word?
        line_idx, start_idx, end_idx = -1, -1, -1
        for info in word_infos[0]:
            if info['sentence_idx'] == sentence_idx:
                line_idx = info["line_idx"]
                start_idx = info["start"]
                break
        for info in word_infos[-1]:
            if info['sentence_idx'] == sentence_idx:
                end_idx = info['end']
                break
        res = build_search_result_info(sentences, line_idx, start_idx, end_idx, sentence_idx)
        occurencies.append(res)

    return occurencies

def searchText(filename, searchContent):
    print("searching text")
    searchContent = searchContent.replace("%20", " ")
    word_in_search = word_tokenize(searchContent)
    occurencies = generalSearchText(filename, word_in_search)

    res_dict = {}
    res_dict["query_text"] = searchContent
    res_dict["number_of_occurrences"] = len(occurencies)
    res_dict["occurences"] = occurencies
    return res_dict

def searchTextWithPrefixAtTail(filename, searchContent):
    print("searching text with prefix at tail----")
    searchContent = searchContent.replace("%20", " ")
    word_in_search = word_tokenize(searchContent)
    # treat the last word as prefix and search it in trie tree
    occurencies = generalSearchText(filename, word_in_search)

    res_dict = {}
    res_dict["query_text"] = searchContent
    res_dict["number_of_occurrences"] = len(occurencies)
    res_dict["occurences"] = occurencies
    return res_dict