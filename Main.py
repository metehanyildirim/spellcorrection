from RegexFilter import RegexFilter
from EditDistance import EditDistance
from Unigram import Unigram
from Bigram import Bigram
from Graph import Graph
from Graph import Vertex
import re
import time
import sys

dataset = open(sys.argv[1])
output = open(sys.argv[2], "w")
spaced = []
words = ""
wordList = []
for line in dataset:
    words += " " + line
    wordList.extend(line.split())

#Correct words
correctString = words
m = re.search('<ERR targ=(.+?)>[^(</ERR>)]*</ERR>', correctString)
while(m != None):
    correctString = re.sub(re.escape(m.group(0)), "<" + m.group(1).replace(" ", "#") + ">", correctString)
    m = re.search('<ERR targ=(.+?)>[^<]*</ERR>', correctString)

correctWords = correctString.lower().split()
correctionIndexes = []
for counter , word in enumerate(correctWords):
    m = re.match("<([^>]*)>", word)
    if(m):
        correctionIndexes.append(counter)
        correctWords[counter] = m.group(1).strip(".").strip("!").strip(",").lower().replace("#", " ")


### Our word array with incorrect words.
start_indices = [i for i, x in enumerate(wordList) if x == "<ERR"]
end_indices = [i for i, x in enumerate(wordList) if x == "</ERR>"]
origWords = [x.strip(",") for x in wordList]
for i in range(len(start_indices)):
    origWords[start_indices[i]] = ' '.join(wordList[start_indices[i]:end_indices[i] + 1])
    m = re.search('<ERR targ=.*>(.+?)</ERR>', origWords[start_indices[i]])
    if(m):
        origWords[start_indices[i]] = m.group(1).strip().lower()
i = 0
delete = False
while i < len(origWords):
    if(origWords[i].startswith("targ=")):
        while(origWords[i] != "</ERR>"):
            del origWords[i]
        del origWords[i]
        i += 1
    else:
        i += 1




### Let's form our bigram.
unigram = Unigram(correctWords)
bigram = Bigram(correctWords, unigram)
lettersMap = {}

lettersMap[EditDistance.WORDBOUNDARY] = len(correctWords)
for word in correctWords:
    for i in range(len(word)):
        lettersMap[word[i]] = lettersMap.get(word[i] , 0) + 1
    lettersMap[(EditDistance.WORDBOUNDARY + word[0])] = lettersMap.get((EditDistance.WORDBOUNDARY + word[0]), 0) + 1
    for i in range(len(word) - 1):
        lettersMap[(word[i] + word[i + 1])] = lettersMap.get((word[i] + word[i + 1]) , 0) + 1

# This is for creating the edit distances. They return a hashmap with a tuple like this: ('ins', 'a', 'ab') -> 22
changeMap = {}
wrongWordsSet = set([origWords[i] for i in correctionIndexes])
start = time.time()
for wrongWord in wrongWordsSet:
    for word in unigram.occurences.keys():
        if(len(wrongWord) < len(word) - 1 or len(wrongWord) > len(word) + 1):
            continue
        tuple = EditDistance.findDistance(wrongWord, word)
        if(tuple != None):
            tupletized = EditDistance.tupletize(tuple, wrongWord , word)
            changeMap[tupletized] = changeMap.get(tupletized, 0) + unigram.occurences[word] * 1

# This divides the counts to our values on our tuples to get our emission probabilities.
emissions = {}
for key, value in changeMap.items():
    emissions[key] = value / float(lettersMap[key[1]])
changeMap = None
print("Edit distance calculations took " + str(time.time() - start) + " seconds")


# Building hmm and implementing viterbi.
graphs = []
graph = Graph()
layer = 1
id = 1
for i in range(len(origWords)):
    # When we see end of sentence
    if (origWords[i] == "." or origWords[i] == "!" or origWords[i] == "?"):
        graph.add_node(Vertex(id, layer, origWords[i], 1))
        layer = 1
        id = 1
        graphs.append(graph)
        graph = Graph()
        continue
    if(i in correctionIndexes):
        found = False
        for word in unigram.occurences.keys():
            if (len(origWords[i]) < len(word) - 1 or len(origWords[i]) > len(word) + 1):
                continue
            tuple = EditDistance.findDistance(origWords[i], word)
            if (tuple != None):
                tupletized = EditDistance.tupletize(tuple, origWords[i], word)
                graph.add_node(Vertex(id, layer, word, emissions[tupletized]))
                found = True
                id += 1
        if(not found):
            graph.add_node(Vertex(id, layer, origWords[i], 1))
            id += 1
    else:
        graph.add_node(Vertex(id, layer, origWords[i], 1))
        id += 1
    layer += 1


# Forward viterbi.
guesses = []
for graph in graphs:
    graph.calculateInitials(unigram)
    graph.calculateProbabilities(bigram)
    guesses.extend(graph.getSentence())
    output.write(' '.join(graph.getSentence()))


with open("wordstuff", "w") as f:
    for i in correctionIndexes:
        f.write(correctWords[i] + " " + guesses[i] + "\n")


pay = 0
payda = len(correctionIndexes)
for i in correctionIndexes:
    if(correctWords[i] == guesses[i]):
        pay += 1

output.write(str(float(pay) / payda))
print(str(float(pay) / payda))

dataset.close()
output.close()