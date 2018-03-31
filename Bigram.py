from collections import OrderedDict
from random import *
import math

'''
This class implements the bigram.
unigram: This is the already implemented unigram class we need this to reuse some stuff.
words: word list as an array.

To implement bigram we will do as follows:
Implement a hashmap of hashmap. First hashmap is for storing the preceding word as key.
Second hashmap has the second word as key and its probability as value.
'''
class Bigram:
    def __init__(self, words, unigram):
        self.occurrence_map = {}
        self.frequency = unigram.occurences
        self.unigram = unigram
        for x in range(len(words) - 1):
            if(words[x] not in self.occurrence_map):
                self.occurrence_map[words[x]] = {}
                self.occurrence_map[words[x]][words[x+1]] = 1
            else:
                if(words[x + 1] in self.occurrence_map[words[x]]):
                    self.occurrence_map[words[x]][words[x + 1]] += 1
                else:
                    self.occurrence_map[words[x]][words[x + 1]] = 1

    def getProbability(self, preword, postword, smoothing):
        numerator = self.occurrence_map.get(preword, 0)
        numerator = numerator.get(postword, 0) if  preword in self.occurrence_map else 0
        denumerator = sum(self.occurrence_map[preword].values()) if preword in self.occurrence_map else 1
        if smoothing:
            return float(numerator + 1) / (denumerator + len(self.frequency))
        else:
            return float(numerator) / denumerator