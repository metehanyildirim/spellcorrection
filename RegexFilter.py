import re

class RegexFilter:
    def __init__(self):
        self.regexes = []

    def addFilter(self, regex):
        self.regexes.append(re.compile(regex))

    def isRejected(self, string):
        matched = list(filter(lambda x: x == False ,map(lambda x: not re.match(x, string), self.regexes)))
        return len(matched)