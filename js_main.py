
import os
import json
import pickle
import jieba
from operator import itemgetter

stop_words = set()
all_word_dict = {}
invert_index = {}
article_dict = {}
word_id = 0
article_id = 0

def load_stopwords():
    with open("./stop_words_tf") as fin:
        for line in fin:
            stop_words.add(line[:-1])


def process_one_line(line, article_word_vector):
    global word_id
    #line_words = line.lower().replace("\'", "").replace(",", "").replace(".", "").replace("!", "").split(' ')
    line_words = filter(lambda x: len(x) > 0 and x != ' ',jieba.cut(line.lower()))
    #print(line, ",".join(line_words))
    for word in line_words:
        if word in stop_words:
            continue
        if not word.isalpha():
            continue
        if word not in all_word_dict:
            word_id += 1
            all_word_dict[word] = word_id
        if word not in article_word_vector:
            article_word_vector[word] = 0
        article_word_vector[word] += 1


def load_datasets():
    global article_id
    for dirpath, _, filenames in os.walk('./js_datasets'):
        for filename in filenames:
            print(f"Loading {filename}")
            article_id += 1
            article_word_vector = {}
            process_one_line(filename.replace("_", " "), article_word_vector)
            with open(os.path.join(dirpath, filename), "r") as fin:
                for line in fin:
                    process_one_line(line, article_word_vector)
                fin.close()
            article_dict[article_id] = (filename, article_word_vector)


# def load_News_Category_Dataset_v3():
#     global article_id
#     with open("./News_Category_Dataset_v3.json", "r") as fin:
#         for line in fin:
#             article_id += 1
#             article_word_vector = {}
#             json_str = json.loads(line[:-1])
#             process_one_line(json_str["headline"], article_word_vector)
#             process_one_line(json_str["short_description"], article_word_vector)
#             article_dict[article_id] = (json_str["headline"], article_word_vector)


def build_invert_index():
    # Too slow to optimal
    # for word, _ in all_word_dict.items():
    #     invert_index_row = set()
    #     for article_id, article in article_dict.items():
    #         _, article_word_vector = article
    #         if word in article_word_vector:
    #             invert_index_row.add(article_id)
    #     invert_index[word] = invert_index_row

    for article_id, article in article_dict.items():
        _, article_word_vector = article
        for word in article_word_vector:
            if word not in invert_index:
                invert_index[word] = set()
            invert_index[word].add(article_id)


def ask_for_searching():
    while True:
        search_key_words = input("Enter search key words: ")
        print("=============================================")
        key_words = search_key_words.lower().split(" ")
        article_result = None
        for key_word in key_words:
            if key_word not in all_word_dict:
                print(f"Key word {key_word} not in any article, search engine ignore it.")
                continue
            if article_result is None:
                article_result = invert_index[key_word]
            else:
                next_invert_article = invert_index[key_word]
                article_result = article_result.intersection(next_invert_article)

        if not article_result or len(article_result) == 0:
            print("Can't find any article for search key words.")
        else:
            print(f"Key words: {' '.join(key_words)}, find in fellow articles:")
            # TODO rank
            rank_article_result = []
            for article_id in article_result:
                rank_article_result.append((float(article_dict[article_id][0].split('_')[0]), article_id))

            rank_article_result = sorted(rank_article_result, key=itemgetter(0), reverse=True)

            for _, article_id in rank_article_result:
                print(article_dict[article_id][0], ":")
                for key_word in key_words:
                    if key_word not in all_word_dict:
                        continue
                    print({key_word}, '\n', getCodeSegmentFromFile(article_dict[article_id][0], key_word))


def getCodeSegmentFromFile(filename, search_key_word):
    BEFORE_LINE = 5
    AFTER_LINE = 5
    file_content = []
    content_result = []
    with open(os.path.join("./js_datasets", filename), "r") as fin:
        for line in fin:
            file_content.append(line)
        fin.close()

    for line_num, line in enumerate(file_content):
        # print(line)
        if line.find(search_key_word) != -1:
            # content_result.append(f'{line_num}:{line}')
            content_result.append("".join(file_content[max(line_num - BEFORE_LINE, 0):min(line_num + AFTER_LINE, len(file_content))]))

    return "====================\n".join(content_result)





if __name__ == '__main__':
    load_stopwords()
    # print(stop_words)
    load_datasets()
    #load_News_Category_Dataset_v3()
    print("All word in dictionary contains", len(all_word_dict))
    # print("All article contains", article_dict)
    # print(all_word_dict)
    build_invert_index()
    # print(invert_index)
    ask_for_searching()