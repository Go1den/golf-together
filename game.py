from course import Course

class Game:
    def __init__(self, name: str = 'Unknown Game', courses: list[Course] = None):
        self.name = name
        self.courses = courses if courses else []
