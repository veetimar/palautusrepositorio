import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search(self):
        found = self.stats.search("Kurri")
        self.assertEqual(found.name, "Kurri")

    def test_search_non_existent(self):
        player = self.stats.search("Maija")
        self.assertIsNone(player)

    def test_team(self):
        found = self.stats.team("EDM")
        self.assertEqual(len(found), 3)
        self.assertEqual(found[0].name, "Semenko")
        self.assertEqual(found[1].name, "Kurri")
        self.assertEqual(found[2].name, "Gretzky")

    def test_top(self):
        players = self.stats.top(2)
        self.assertEqual(len(players), 3)
        self.assertEqual(players[0].name, "Gretzky")
        self.assertEqual(players[1].name, "Lemieux")
