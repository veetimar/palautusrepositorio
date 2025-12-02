from statistics import Statistics
from player_reader import PlayerReader
from querybuilder import QueryBuilder
from matchers import All, And, HasAtLeast, HasFewerThan, Not, Or, PlaysIn

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    if False:

        matcher = And(
            HasAtLeast(5, "goals"),
            HasAtLeast(20, "assists"),
            PlaysIn("PHI")
        )

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        matcher = And(
            Not(HasAtLeast(2, "goals")),
            PlaysIn("NYR")
        )

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        matcher = And(
            HasFewerThan(2, "goals"),
            PlaysIn("NYR")
        )

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        filtered_with_all = stats.matches(All())
        print(len(filtered_with_all))

        print("----------------------")

        matcher = Or(
            HasAtLeast(45, "goals"),
            HasAtLeast(70, "assists")
        )

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        matcher = And(
            HasAtLeast(70, "points"),
            Or(
                PlaysIn("COL"),
                PlaysIn("FLA"),
                PlaysIn("BOS")
            )
        )

        for player in stats.matches(matcher):
            print(player)

    else:
        query = QueryBuilder()
        matcher = query.build()

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        query = QueryBuilder()

        matcher = query.plays_in("NYR").build()

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        query = QueryBuilder()

        matcher = query.plays_in("NYR").has_at_least(10, "goals").has_fewer_than(20, "goals").build()

        for player in stats.matches(matcher):
            print(player)

        print("----------------------")

        query = QueryBuilder()

        matcher = (
            query
            .one_of(
            query.plays_in("PHI")
                .has_at_least(10, "assists")
                .has_fewer_than(10, "goals"),
            query.plays_in("EDM")
                .has_at_least(50, "points")
            )
            .build()
        )

        for player in stats.matches(matcher):
            print(player)

if __name__ == "__main__":
    main()
