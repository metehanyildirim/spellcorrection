class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}


    def add_node(self, vertex):
        self.nodes.append(vertex)

    def add_edge(self, source, dest, dist):
        self.edges[source] = (dest, dist)

    def __str__(self):
        return str(self.nodes)

    # This function is for calculating probabities at the beginning of our sentence.
    def calculateInitials(self, unigram):
        for vertex in self.nodes:
            if(vertex.layer == 1):
                vertex.probability *= unigram.getProbability(vertex.word)

    def calculateProbabilities(self, bigram):
        for i in range(2, self.nodes[-1].layer + 1):
            layerednodes = [x for x in self.nodes if x.layer == i]
            prevnodes = [x for x in self.nodes if x.layer == i - 1]
            self.calculateLayerProbs(layerednodes, prevnodes, bigram)

    def calculateLayerProbs(self, layerednodes , prevnodes, bigram):
        for curr in layerednodes:
            probs = [prev.probability * bigram.getProbability(prev.word, curr.word, True) * prev.emission for prev in prevnodes] # Calculate probability.
            maximumProb = max(probs)
            index = probs.index(maximumProb)
            self.add_edge(curr.id, prevnodes[index], maximumProb)

    def getSentence(self):
        ourSentence = []
        ourNode = self.nodes[-1]
        ourLayer = ourNode.layer
        while(ourLayer != 1):
            ourSentence.append(ourNode.word)
            ourNode = self.edges[ourNode.id][0]
            ourLayer = ourNode.layer
        ourSentence.append(ourNode.word)
        ourSentence.reverse()
        return ' '.join(ourSentence)




class Vertex:
    def __init__(self, id, layer, word, emission):
        self.id = id
        self.layer = layer
        self.word = word
        self.emission = emission
        self.probability = 1

    def __str__(self):
        return str(self.id) + " " + str(self.layer) + " " + str(self.word) + " " + str(self.emission)