from flask import Flask, render_template_string, request, redirect, url_for

from tuomari import Tuomari
from tekoaly import Tekoaly, TekoalyParannettu

app = Flask(__name__)

# Yksinkertainen, prosessikohtainen pelitila. Ei erillistä käyttäjäkohtaisuutta.
tuomari_pelaaja_vs_pelaaja = Tuomari()
tuomari_tekoaly = Tuomari()
tuomari_parempi_tekoaly = Tuomari()

tekoaly = Tekoaly()
parempi_tekoaly = TekoalyParannettu(10)

SALLITUT_SIIRROT = ("k", "p", "s")


def _onko_ok_siirto(siirto: str) -> bool:
    return siirto in SALLITUT_SIIRROT


INDEX_TEMPLATE = """
<!doctype html>
<html lang="fi">
  <head>
    <meta charset="utf-8" />
    <title>Kivi-Paperi-Sakset - Web</title>
    <style>
      body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e5e7eb; margin: 0; }
      .container { max-width: 800px; margin: 40px auto; padding: 24px; background: #020617; border-radius: 16px; box-shadow: 0 20px 25px -5px rgba(15,23,42,0.8); }
      h1 { margin-top: 0; font-size: 2rem; }
      .modes { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 24px; }
      .card { border-radius: 12px; padding: 16px; background: #0b1120; border: 1px solid #1e293b; display: flex; flex-direction: column; justify-content: space-between; }
      .card h2 { font-size: 1.1rem; margin: 0 0 8px; }
      .card p { font-size: 0.9rem; margin: 0 0 12px; color: #9ca3af; }
      .btn { display: inline-flex; align-items: center; justify-content: center; padding: 8px 14px; border-radius: 999px; border: none; background: linear-gradient(to right, #6366f1, #ec4899); color: white; cursor: pointer; font-weight: 500; font-size: 0.9rem; text-decoration: none; }
      .btn:hover { opacity: 0.9; }
      footer { margin-top: 24px; font-size: 0.8rem; color: #6b7280; text-align: center; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Kivi-Paperi-Sakset - selainversio</h1>
      <p>Valitse pelimuoto. Peli päättyy, kun annat virheellisen siirron (jonkun muun kuin <strong>k</strong>, <strong>p</strong> tai <strong>s</strong>).</p>
      <div class="modes">
        <div class="card">
          <h2>Ihminen vs ihminen</h2>
          <p>Kaksi pelaajaa samalta koneelta.</p>
          <a class="btn" href="{{ url_for('game', mode='pvp') }}">Aloita</a>
        </div>
        <div class="card">
          <h2>Ihminen vs tekoäly</h2>
          <p>Perus tekoäly, joka kiertää siirtoja.</p>
          <a class="btn" href="{{ url_for('game', mode='ai') }}">Aloita</a>
        </div>
        <div class="card">
          <h2>Ihminen vs parannettu tekoäly</h2>
          <p>Tekoäly, joka muistaa aikaisempia siirtojasi.</p>
          <a class="btn" href="{{ url_for('game', mode='better_ai') }}">Aloita</a>
        </div>
      </div>
      <footer>
        Tämä käyttöliittymä käyttää samoja pelilogiikkaluokkia kuin komentoriviversio.
      </footer>
    </div>
  </body>
</html>
"""


GAME_TEMPLATE = """
<!doctype html>
<html lang="fi">
  <head>
    <meta charset="utf-8" />
    <title>Kivi-Paperi-Sakset - Peli</title>
    <style>
      body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e5e7eb; margin: 0; }
      .container { max-width: 800px; margin: 40px auto; padding: 24px; background: #020617; border-radius: 16px; box-shadow: 0 20px 25px -5px rgba(15,23,42,0.8); }
      h1 { margin-top: 0; font-size: 1.7rem; }
      .score { margin: 16px 0; padding: 12px 16px; border-radius: 12px; background: #0b1120; border: 1px solid #1e293b; white-space: pre-line; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
      form { margin-top: 16px; display: grid; gap: 12px; }
      label { font-size: 0.9rem; color: #9ca3af; }
      input[type="text"] { padding: 8px 10px; border-radius: 8px; border: 1px solid #1f2937; background: #020617; color: #e5e7eb; }
      .btn-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
      .btn { display: inline-flex; align-items: center; justify-content: center; padding: 8px 14px; border-radius: 999px; border: none; background: linear-gradient(to right, #6366f1, #ec4899); color: white; cursor: pointer; font-weight: 500; font-size: 0.9rem; text-decoration: none; }
      .btn.secondary { background: #111827; border: 1px solid #374151; }
      .btn.secondary:hover { background: #020617; }
      .hint { font-size: 0.8rem; color: #6b7280; }
      .result { margin-top: 8px; font-size: 0.9rem; color: #a5b4fc; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{{ title }}</h1>

      <div class="score">{{ score }}</div>

      {% if last_move_info %}
      <div class="result">{{ last_move_info }}</div>
      {% endif %}

      <form method="post">
        {% if mode == 'pvp' %}
          <div>
            <label>Ensimmäisen pelaajan siirto (k / p / s)</label>
            <input type="text" name="eka" autofocus required />
          </div>
          <div>
            <label>Toisen pelaajan siirto (k / p / s)</label>
            <input type="text" name="toka" required />
          </div>
        {% else %}
          <div>
            <label>Sinun siirtosi (k / p / s)</label>
            <input type="text" name="eka" autofocus required />
          </div>
        {% endif %}

        <div class="btn-row">
          <button class="btn" type="submit">Pelaa kierros</button>
          <a class="btn secondary" href="{{ url_for('game_reset', mode=mode) }}">Aloita alusta</a>
          <a class="btn secondary" href="{{ url_for('index') }}">Takaisin alkuun</a>
        </div>
        <div class="hint">Peli päättyy, jos annat muun kuin k, p tai s.</div>
      </form>
    </div>
  </body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE)


def _get_tuomari_for_mode(mode: str) -> Tuomari:
    if mode == "pvp":
        return tuomari_pelaaja_vs_pelaaja
    if mode == "ai":
        return tuomari_tekoaly
    if mode == "better_ai":
        return tuomari_parempi_tekoaly
    raise ValueError("Tuntematon pelimuoto")


def _title_for_mode(mode: str) -> str:
    if mode == "pvp":
        return "Ihminen vs ihminen"
    if mode == "ai":
        return "Ihminen vs tekoäly"
    if mode == "better_ai":
        return "Ihminen vs parannettu tekoäly"
    return "Peli"


@app.route("/game/<mode>", methods=["GET", "POST"])
def game(mode):
    if mode not in {"pvp", "ai", "better_ai"}:
        return redirect(url_for("index"))

    tuomari = _get_tuomari_for_mode(mode)
    last_move_info = None

    if request.method == "POST":
        eka = request.form.get("eka", "").strip().lower()

        if mode == "pvp":
            toka = request.form.get("toka", "").strip().lower()
        elif mode == "ai":
            toka = tekoaly.anna_siirto()
        else:  # better_ai
            toka = parempi_tekoaly.anna_siirto()
            parempi_tekoaly.aseta_siirto(eka)

        if not (_onko_ok_siirto(eka) and _onko_ok_siirto(toka)):
            last_move_info = "Peli päättyi virheelliseen siirtoon. Aloita uusi peli, jos haluat jatkaa."
        else:
            tuomari.kirjaa_siirto(eka, toka)
            if mode == "pvp":
                last_move_info = f"Ensimmäinen pelaaja: {eka}, toinen pelaaja: {toka}"
            else:
                last_move_info = f"Sinä: {eka}, tietokone: {toka}"

    return render_template_string(
        GAME_TEMPLATE,
        mode=mode,
        title=_title_for_mode(mode),
        score=str(tuomari),
        last_move_info=last_move_info,
    )


@app.route("/game/<mode>/reset")
def game_reset(mode):
    if mode not in {"pvp", "ai", "better_ai"}:
        return redirect(url_for("index"))

    tuomari = _get_tuomari_for_mode(mode)
    tuomari._ekan_pisteet = 0  # noqa: SLF001
    tuomari._tokan_pisteet = 0  # noqa: SLF001
    tuomari._tasapelit = 0  # noqa: SLF001

    if mode == "ai":
        global tekoaly  # noqa: PLW0603
        tekoaly = Tekoaly()
    elif mode == "better_ai":
        global parempi_tekoaly  # noqa: PLW0603
        parempi_tekoaly = TekoalyParannettu(10)

    return redirect(url_for("game", mode=mode))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
