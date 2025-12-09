from kps import KPS


def main():
    while True:
        peli = hae_peli()
        if peli is None:
            break
        print("Peli loppuu, kun jompikumpi pelaajista on voittanut 5 kertaa ")
        print("tai pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s")
        peli.pelaa()


def hae_peli():
    print("Valitse pelataanko"
          "\n (a) Ihmistä vastaan"
          "\n (b) Tekoälyä vastaan"
          "\n (c) Parannettua tekoälyä vastaan"
          "\nMuilla valinnoilla lopetetaan"
          )
    vastaus = input()
    if vastaus.endswith("a"):
        return KPS.pelaaja_vs_pelaaja()
    elif vastaus.endswith("b"):
        return KPS.tekoaly()
    elif vastaus.endswith("c"):
        return KPS.parempi_tekoaly()
    else:
        return None


if __name__ == "__main__":
    main()
