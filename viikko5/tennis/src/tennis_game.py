class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_points += 1
        elif player_name == "player2":
            self.player2_points += 1
        else:
            raise ValueError(f"Invalid player name: {player_name}")

    def get_score(self):
        if self.player1_points == self.player2_points:
            score = self._equal_score()
        elif self.player1_points >= 4 or self.player2_points >= 4:
            score = self._advantage_or_win_score()
        else:
            score = self._normal_score()
        return score

    def _equal_score(self):
        if self.player1_points == 0:
            score = "Love-All"
        elif self.player1_points == 1:
            score = "Fifteen-All"
        elif self.player1_points == 2:
            score = "Thirty-All"
        else:
            score = "Deuce"
        return score

    def _advantage_or_win_score(self):
        margin = self.player1_points - self.player2_points
        if margin == 1:
            score = "Advantage player1"
        elif margin == -1:
            score = "Advantage player2"
        elif margin >= 2:
            score = "Win for player1"
        else:
            score = "Win for player2"
        return score

    def _normal_score(self):
        player1_score = self._format_points(self.player1_points)
        player2_score = self._format_points(self.player2_points)
        score = f"{player1_score}-{player2_score}"
        return score

    def _format_points(self, points):
        if points == 0:
            score_name = "Love"
        elif points == 1:
            score_name = "Fifteen"
        elif points == 2:
            score_name = "Thirty"
        elif points == 3:
            score_name = "Forty"
        return score_name
