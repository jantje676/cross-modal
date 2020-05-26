# -----------------------------------------------------------
# Stacked Cross Attention Network implementation based on
# https://arxiv.org/abs/1803.08024.
# "Stacked Cross Attention for Image-Text Matching"
# Kuang-Huei Lee, Xi Chen, Gang Hua, Houdong Hu, Xiaodong He
#
# Writen by Kuang-Huei Lee, 2018
# ---------------------------------------------------------------
"""Vocabulary wrapper"""

import nltk
from collections import Counter
import argparse
import os
import json
import csv

annotations = {
    'Fashion200K': ['train', 'dev']
}


class Vocabulary(object):
    """Simple vocabulary wrapper."""

    def __init__(self):
        self.word2idx = {}
        self.idx2word = {}
        self.idx = 0

    def add_word(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = self.idx
            self.idx2word[self.idx] = word
            self.idx += 1

    def __call__(self, word):
        if word not in self.word2idx:
            return self.word2idx['<unk>']
        return self.word2idx[word]

    def __len__(self):
        return len(self.word2idx)


def serialize_vocab(vocab, dest):
    d = {}
    d['word2idx'] = vocab.word2idx
    d['idx2word'] = vocab.idx2word
    d['idx'] = vocab.idx
    with open(dest, "w") as f:
        json.dump(d, f)


def deserialize_vocab(src):
    with open(src) as f:
        d = json.load(f)
    vocab = Vocabulary()
    vocab.word2idx = d['word2idx']
    vocab.idx2word = d['idx2word']
    vocab.idx = d['idx']
    return vocab


def from_txt(txt):
    captions = []
    with open(txt, 'r', newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            captions.append(line[1].strip())
    return captions



def build_vocab(data_path, data_name, version, caption_file, threshold):
    """Build a simple vocabulary wrapper."""
    counter = Counter()
    for path in caption_file[data_name]:
        full_path = "{}/data_captions_{}_{}.txt".format(data_path,version, path)
        captions = from_txt(full_path)
        for i, caption in enumerate(captions):
            tokens = nltk.tokenize.word_tokenize(
                caption.lower())
            counter.update(tokens)

            if i % 1000 == 0:
                print("[%d/%d] tokenized the captions." % (i, len(captions)))

    # Discard if the occurrence of the word is less than min_word_cnt.
    words = [word for word, cnt in counter.items() if cnt >= threshold]

    # Create a vocab wrapper and add some special tokens.
    vocab = Vocabulary()
    vocab.add_word('<pad>')
    vocab.add_word('<start>')
    vocab.add_word('<end>')
    vocab.add_word('<unk>')

    # Add words to the vocabulary.
    for i, word in enumerate(words):
        vocab.add_word(word)
    return vocab


def main(data_path, data_name, version, clothing):
    data_path = "../data/Fashion200K/{}/".format(clothing)
    data_name = "Fashion200K"
    vocab = build_vocab(data_path, data_name, version, caption_file=annotations, threshold=1)
    serialize_vocab(vocab, '../vocab/{}/{}_vocab_{}.json'.format(clothing, data_name, version))
    print("Saved vocabulary file to ", '../vocab/{}/{}_vocab_{}.json'.format(clothing, data_name, version))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='data')
    parser.add_argument('--data_name', default='f30k_precomp', help='{coco,f30k}_precomp')
    parser.add_argument('--version', default=None, help='version')
    parser.add_argument('--clothing', default=None, help='clothing')


    opt = parser.parse_args()
    main(opt.data_path, opt.data_name, opt.version, opt.clothing)
