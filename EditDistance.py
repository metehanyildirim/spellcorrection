

class EditDistance:

    WORDBOUNDARY = "#"

    @staticmethod
    def findDistance(misspelled, word):
        if (len(misspelled) < len(word) - 1 or len(misspelled) > len(word) + 1):
            return None
        i , k = 0 , 0
        cost = 0
        tuple = None
        while(i < len(word) and k < len(misspelled)):
            if(word[i] == misspelled[k]):
                i += 1
                k += 1
            else:
                cost += 1
                if(len(word) > len(misspelled)):
                    tuple = ('del' , i, k)
                    i += 1
                elif(len(misspelled) > len(word)):
                    tuple = ('ins', i, k)
                    k += 1
                else:
                    tuple = ('sub', i, k)
                    i += 1
                    k += 1
            if(cost > 1):
                return None
        return tuple

    @staticmethod
    def tupletize(tuple, misspelled, word):
        if(tuple[0] == "ins"):
            ourtuple = tuple[1]
            right = EditDistance.WORDBOUNDARY + misspelled[ourtuple] if (ourtuple == 0) else misspelled[ourtuple - 1] + misspelled[ourtuple]
            left = EditDistance.WORDBOUNDARY if(ourtuple == 0) else misspelled[ourtuple - 1]
            return ('ins', left, right)
        elif(tuple[0] == "del"):
            ourtuple = tuple[2]
            left = EditDistance.WORDBOUNDARY + word[ourtuple] if (ourtuple == 0) else word[ourtuple - 1] + word[ourtuple]
            right = EditDistance.WORDBOUNDARY if(ourtuple == 0) else misspelled[ourtuple - 1]
            return ('del', left, right)
        else:
            return ('sub', word[tuple[1]], misspelled[tuple[1]])


class Node:
    def __init__(self, isLeft = False, isDiag = False, isUp = False):
        self.isLeft = isLeft
        self.isDiag = isDiag
        self.isUp = isUp