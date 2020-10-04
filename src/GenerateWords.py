#encoding=utf-8
import re
import os
import glob
import json

from NepaliTokenizer import Tokenizer


def get_text_data():
    files = glob.glob('corpus/**/*', recursive=True)
    for file in files:
        if os.path.isfile(file):
            with open(file, 'r') as fp:
                yield fp.read()


def tokenize(text):
    additional_split_chars = ['–', '‘', '’', '…']
    chars_to_be_removed = r'[^ऀ-ॿ]|[०-९]'

    tokens = Tokenizer().word_tokenize(text, new_punctuation=additional_split_chars)
    tokens = [re.sub(chars_to_be_removed, '', word) for word in tokens]
    tokens = [token for token in tokens if token]
    return tokens


def generate_transliterals_templates():
    tokens = set()
    for text in get_text_data():
        tokens.update(tokenize(text))

    tokens = list(tokens)
    words_per_file = 20
    for i in range((len(tokens) // words_per_file)):
        dictionary_template = (dict(zip(tokens[i * words_per_file: (i+1) * words_per_file], [''] * words_per_file)))
        json.dump(dictionary_template, open("../transliterals/transliteral_words_{:03d}.json".format(i), 'w'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    print(generate_transliterals_templates())

