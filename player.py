class Player:
    def __init__(self, name: str = '', address: str = '', scoreList: list[int] = None):
        self.name = name
        self.address = address
        self.scoreList = scoreList if scoreList else []
