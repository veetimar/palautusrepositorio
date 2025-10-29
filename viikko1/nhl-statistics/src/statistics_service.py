from player_reader import PlayerReader
from enum import Enum

class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3

class StatisticsService:
    def __init__(self, reader: PlayerReader):
        self._players = reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name):
        players_of_team = filter(
            lambda player: player.team == team_name,
            self._players
        )

        return list(players_of_team)

    def top(self, how_many, by=SortBy.POINTS):
        # metodin käyttämä apufufunktio voidaan määritellä näin
        def sort_by_points(player):
            return player.points
        
        def sort_by_goals(player):
            return player.goals
        
        def sort_by_assists(player):
            return player.assists
        
        if by == SortBy.POINTS:
            key = sort_by_points
        elif by == SortBy.GOALS:
            key = sort_by_goals
        elif by == SortBy.ASSISTS:
            key = sort_by_assists
        else:
            raise ValueError

        sorted_players = sorted(
            self._players,
            reverse=True,
            key=key
        )

        result = []
        i = 0
        while i <= how_many:
            result.append(sorted_players[i])
            i += 1

        return result
