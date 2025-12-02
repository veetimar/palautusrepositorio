class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvot = [arvo]

    def miinus(self, operandi):
        self._arvot.append(self._arvot[-1] - operandi)

    def plus(self, operandi):
        self._arvot.append(self._arvot[-1] + operandi)

    def nollaa(self):
        self._arvot.append(0)

    def aseta_arvo(self, arvo):
        self._arvot.append(arvo)

    def kumoa(self):
        if len(self._arvot) > 1:
            self._arvot.pop()

    def arvo(self):
        return self._arvot[-1]
