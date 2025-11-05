class Player:
    def __init__(self, p_dict):
        self.name = p_dict['name']
        self.nationality = p_dict['nationality']
        self.assists = p_dict['assists']
        self.goals = p_dict['goals']
        self.team = p_dict['team']
        self.games = p_dict['games']
        self.points = self.assists + self.goals

    def do_nothing(self):
        pass

    def __str__(self):
        return f"{self.name:20}{self.team:20}{self.goals:2} + {self.assists:2} = {self.points}"
