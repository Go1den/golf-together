class Course:
    def __init__(self, name: str = 'Unknown Golf Course', parList: list[int] = None):
        self.name = name
        self.parList = parList if parList else []
        self.courseScore = sum(self.parList)
