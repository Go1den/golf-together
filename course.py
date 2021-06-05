class Course:
    def __init__(self, name: str = 'Unknown Golf Course', game: str = '', parList: list[int] = None):
        self.name = name
        self.game = game
        self.parList = parList if parList else []
        self.courseScore = sum(self.parList)
