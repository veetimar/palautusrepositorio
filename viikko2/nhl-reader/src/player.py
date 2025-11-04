class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.games = dict['games']
        if 'id' in dict:
            self.id = dict['id']
        self.points = self.assists + self.goals

    def __str__(self):
        return f"{self.name:20}{self.team:20}{self.goals:2} + {self.assists:2} = {self.points}"
