class Player:
    def __init__(self, name: str = '', uuid: str = '', score: int = 0, parThroughCurrentHole: int = 0, currentHole: int = 0):
        self.name = name
        self.uuid = uuid
        self.score = score
        self.parThroughCurrentHole = parThroughCurrentHole
        self.currentHole = currentHole
        self.scoreAsString = None
        self.setRelativeScore()

    def setRelativeScore(self):
        relScore = self.score - self.parThroughCurrentHole
        if relScore == 0:
            self.scoreAsString = "E"
        elif relScore > 0:
            self.scoreAsString = "+" + str(relScore)
        else:
            self.scoreAsString = str(relScore)

    def print(self):
        print(self.name)
        print(self.uuid)
        print(str(self.score))
        print(str(self.parThroughCurrentHole))
        print(str(self.currentHole))
        print(self.scoreAsString)