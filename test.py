from RadixTree import *
import random
import numpy as np


test_vocab_size = 50000
file_size = 370103
test_vocab_list = []
test_size = 300

with open('words_alpha.txt', 'r') as words_alpha:
    for line in words_alpha:
        if random.random() < test_vocab_size/file_size:
            test_vocab_list.append(str(line.strip()))

test = np.array(test_vocab_list)[np.random.rand(len(test_vocab_list), ) < test_size/test_vocab_size]

test_word_set = set(test)
s = RadixTree(test)
print(set(s) == test_word_set)
print(len(set(s)) == len(s) == len(test))
test_word_set.add('test_element')
s.add_string('test_element')
print('test_element' in s)
