from collections import OrderedDict

class Unigram:
    def __init__(self, words):
        self.occurences =  {}
        for word in words:
            if(word in self.occurences):
                self.occurences[word] += 1
            else:
                self.occurences[word] = 1
        self.sum = 0
        for key in self.occurences:
            self.sum += self.occurences[key]
        prob = 0
        self.probMap = OrderedDict()
        for key in self.occurences:
            prob += self.occurences[key] / self.sum
            self.probMap[prob] = key

    '''
    Returns the probability of certain word.
    '''
    def getProbability(self, word):
        return self.occurences.get(word, 0) / self.sum