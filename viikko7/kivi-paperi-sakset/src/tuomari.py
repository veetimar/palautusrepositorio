class Tuomari:
    def __init__(self):
        self._ekan_pisteet = 0
        self._tokan_pisteet = 0
        self._tasapelit = 0

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self._tasapelit += 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self._ekan_pisteet += 1
        else:
            self._tokan_pisteet += 1

    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True
        return False

    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True
        return False

    def __str__(self):
        return f"Pelitilanne: {self._ekan_pisteet} - {self._tokan_pisteet}\nTasapelit: {self._tasapelit}"
