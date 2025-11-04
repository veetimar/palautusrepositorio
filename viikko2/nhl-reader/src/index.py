import requests
from rich import print, console, table
from player import Player
input = console.Console().input

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        players = [Player(player_dict) for player_dict in response]
        return players

class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        nationality = nationality.casefold()
        filtered = filter(lambda p: p.nationality.casefold() == nationality, self.players)
        top = sorted(filtered, key=lambda p: p.points, reverse=True)
        return top

def main():
    season = input(f"Season [wheat1][2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26][/wheat1] [cyan](2024-25)[/cyan]: ")
    if not season:
        season = "2024-25"
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    while True:
        nationality = input("Nationality [wheat1][USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS][/wheat1] [cyan]()[/cyan]: ")
        players = stats.top_scorers_by_nationality(nationality)
        tab = table.Table(title=f"[italic]Season {season} players from {nationality.upper()}[/italic]")
        tab.add_column("Released", style="dim")
        tab.add_column("teams", style="dim")
        tab.add_column("goals", justify="right", style="green")
        tab.add_column("assists", justify="right", style="green")
        tab.add_column("points", justify="right", style="green")
        for p in players:
            tab.add_row(p.name, p.team, str(p.goals), str(p.assists), str(p.points))
        print(tab)

if __name__ == "__main__":
    main()
