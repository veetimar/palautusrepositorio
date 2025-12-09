import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from web_app import app, _get_tuomari_for_mode


@pytest.fixture(name="client")
def client_fixture():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Kivi-Paperi-Sakset - selainversio" in html
    assert "Ihminen vs ihminen" in html
    assert "Ihminen vs tekoäly" in html
    assert "Ihminen vs parannettu tekoäly" in html


@pytest.mark.parametrize("mode", ["pvp", "ai", "better_ai"])
def test_game_page_get_loads_for_all_modes(client, mode):
    response = client.get(f"/game/{mode}")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Pelitilanne" in html


def test_invalid_mode_redirects_to_index(client):
    response = client.get("/game/unknown", follow_redirects=False)
    assert response.status_code in (301, 302)
    assert "/" in response.headers["Location"]


def test_valid_round_updates_score_pvp(client):
    tuomari = _get_tuomari_for_mode("pvp")
    # nollataan pisteet mahdollisen aiemman testin jäljiltä
    tuomari._ekan_pisteet = 0
    tuomari._tokan_pisteet = 0
    tuomari._tasapelit = 0

    response = client.post("/game/pvp", data={"eka": "k", "toka": "s"})
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # ekan pelaajan pitäisi johtaa 1-0
    assert "Pelitilanne: 1 - 0" in html


def test_invalid_move_shows_game_over_message(client):
    response = client.post("/game/ai", data={"eka": "x"})
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Peli päättyi virheelliseen siirtoon" in html


def test_reset_route_resets_scores(client):
    tuomari = _get_tuomari_for_mode("ai")
    # kasvatetaan pisteitä
    client.post("/game/ai", data={"eka": "k"})

    response = client.post("/game/ai/reset", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # nollatut pisteet
    assert "Pelitilanne: 0 - 0" in html


def test_game_stops_scoring_after_five_wins_pvp(client):
    tuomari = _get_tuomari_for_mode("pvp")
    tuomari._ekan_pisteet = 0
    tuomari._tokan_pisteet = 0
    tuomari._tasapelit = 0

    # eka pelaaja voittaa viisi kierrosta peräkkäin
    for _ in range(5):
        client.post("/game/pvp", data={"eka": "k", "toka": "s"})

    response = client.post("/game/pvp", data={"eka": "k", "toka": "s"})
    html = response.get_data(as_text=True)

    # pisteiden ei pitäisi enää kasvaa yli viiden
    assert "Pelitilanne: 5 - 0" in html
    assert "Peli on jo päättynyt, koska joku on voittanut 5 kertaa" in html
