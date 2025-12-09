from abc import ABC, abstractmethod
from tuomari import Tuomari
from tekoaly import Tekoaly, TekoalyParannettu


class KPS(ABC):
    def __init__(self):
        self.tuomari = Tuomari()

    def pelaa(self):
        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)
        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)
            self.tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(self.tuomari)
        print("Kiitos!")
        print(self.tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    @abstractmethod
    def _toisen_siirto(self, eka):
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"

    @staticmethod
    def pelaaja_vs_pelaaja():
        return KPSPelaajaVsPelaaja()

    @staticmethod
    def tekoaly():
        return KPSTekoaly()

    @staticmethod
    def parempi_tekoaly():
        return KPSParempiTekoaly()


class KPSPelaajaVsPelaaja(KPS):
    def _toisen_siirto(self, eka):
        return input("Toisen pelaajan siirto: ")

class KPSTekoaly(KPS):
    def __init__(self):
        super().__init__()
        self.vastustaja = Tekoaly()

    def _toisen_siirto(self, eka):
        siirto = self.vastustaja.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto

class KPSParempiTekoaly(KPS):
    def __init__(self):
        super().__init__()
        self.vastustaja = TekoalyParannettu(10)

    def _toisen_siirto(self, eka):
        siirto = self.vastustaja.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        self.vastustaja.aseta_siirto(eka)
        return siirto
