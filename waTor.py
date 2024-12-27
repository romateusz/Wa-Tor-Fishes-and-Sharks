import random
import numpy as np
import matplotlib.pyplot as plt

class Organizm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wiek = 1


class Ryba(Organizm):
    def __init__(self, x, y, czas_rozmnazania):
        super().__init__(x, y)
        self.czas_rozmnazania = czas_rozmnazania

    def czy_rozmnazanie(self):
        return self.wiek % self.czas_rozmnazania == 0
    

class Rekin(Organizm):
    def __init__(self, x, y, energia_poczatkowa, czas_rozmnazania):
        super().__init__(x, y)
        self.energia = energia_poczatkowa
        self.czas_rozmnazania = czas_rozmnazania

    def czy_umiera(self):
        return self.energia <= 0

    def czy_rozmnazanie(self):
        return self.wiek % self.czas_rozmnazania == 0


class Plansza:
    def __init__(self, rozmiar, max_iter, czas_rozmnazania_ryb, czas_rozmnazania_rekina, energia_rekina):
        self.rozmiar = rozmiar
        self.siatka = [[None for _ in range(rozmiar)] for _ in range(rozmiar)]
        self.pusta_siatka = []
        self.organizmy = []
        for x in range(rozmiar):
            for y in range(rozmiar):
                self.pusta_siatka.append((x,y))
        self.max_iter = max_iter
        self.czas_rozmnazania_ryb = czas_rozmnazania_ryb
        self.czas_rozmnazania_rekina = czas_rozmnazania_rekina
        self.energia_rekina = energia_rekina

    def dodaj_rybe(self):
        x, y = random.sample(self.pusta_siatka, 1)[0]
        self.pusta_siatka.remove((x, y))
        r = Ryba(x, y, self.czas_rozmnazania_ryb)
        self.siatka[x][y] = r
        self.organizmy.append(r)

    def dodaj_rekina(self):
        x, y = random.sample(self.pusta_siatka, 1)[0]
        self.pusta_siatka.remove((x, y))
        r = Rekin(x, y, self.energia_rekina, self.czas_rozmnazania_rekina)
        self.siatka[x][y] = r
        self.organizmy.append(r)
    
    def ruch_ryby(self, ryba):
        # ruch fizyczny #
        ruchy = [(ryba.x+1, ryba.y), (ryba.x-1, ryba.y), (ryba.x, ryba.y+1), (ryba.x, ryba.y-1)]
        st_x, st_y = ryba.x, ryba.y
        while len(ruchy) > 0:
            x, y = random.sample(ruchy, 1)[0]
            ruchy.remove((x, y))
            x = x % self.rozmiar
            y = y % self.rozmiar
            if self.siatka[x][y] == None:
                self.siatka[ryba.x][ryba.y] = None
                ryba.x, ryba.y = x, y
                self.siatka[x][y] = ryba
                break

        # rozmnażanie #
        if ryba.czy_rozmnazanie():
            if st_x != ryba.x or st_y != ryba.y:
                nowa_ryba = Ryba(st_x, st_y, self.czas_rozmnazania_ryb)
                self.siatka[st_x][st_y] = nowa_ryba
                self.organizmy.append(nowa_ryba)
        ryba.wiek += 1


    def ruch_rekina(self, rekin):
        # spadek energii
        if rekin.czy_umiera():
            self.organizmy.remove(rekin)
            self.siatka[rekin.x][rekin.y] = None
        else:
            rekin.energia -= 1

            # ruch fizyczny i jedzenie rybki #
            ruchy = [((rekin.x+1) % self.rozmiar, rekin.y), ((rekin.x-1) % self.rozmiar, rekin.y), 
                    (rekin.x, (rekin.y+1) % self.rozmiar), (rekin.x, (rekin.y-1) % self.rozmiar)]
            st_x, st_y = rekin.x, rekin.y
            czy_nie_zrobiony_ruch = True
            random.shuffle(ruchy)

            for x, y in ruchy:
                if isinstance(self.siatka[x][y], Ryba):
                    ryba = self.siatka[x][y]
                    self.organizmy.remove(ryba)
                    self.siatka[rekin.x][rekin.y] = None
                    rekin.x, rekin.y = ryba.x, ryba.y
                    self.siatka[x][y] = rekin
                    czy_nie_zrobiony_ruch = False
                    rekin.energia = self.energia_rekina
                    break

            if czy_nie_zrobiony_ruch:
                while len(ruchy) > 0:
                    x, y = random.sample(ruchy, 1)[0]
                    ruchy.remove((x, y))
                    if self.siatka[x][y] == None:
                        self.siatka[rekin.x][rekin.y] = None
                        rekin.x, rekin.y = x, y
                        self.siatka[x][y] = rekin
                        break
            # rozmnażanie #
            if rekin.czy_rozmnazanie():
                if st_x != rekin.x or st_y != rekin.y:
                    nowy_rekin = Rekin(st_x, st_y, self.energia_rekina ,self.czas_rozmnazania_rekina)
                    self.siatka[st_x][st_y] = nowy_rekin
                    self.organizmy.append(nowy_rekin)
            rekin.wiek += 1

    def symuluj(self):
        for iter in range(self.max_iter):
            if iter % 10 == 0:
                print(iter)
                self.wyswietl_plansze(iter)
            for organizm in self.organizmy:
                if isinstance(organizm, Ryba):
                    self.ruch_ryby(organizm)
                else:
                    self.ruch_rekina(organizm)

    def wyswietl_plansze(self, iter):
        result = np.zeros((self.rozmiar, self.rozmiar))
        for x in range(self.rozmiar):
            for y in range(self.rozmiar):
                if isinstance(self.siatka[x][y], Ryba):
                    result[x][y] = 1
                elif isinstance(self.siatka[x][y], Rekin):
                    result[x][y] = -1
        plt.imshow(result, vmin=-1, vmax=1, cmap="bwr")
        plt.savefig(f"img{iter:06d}.png")
        plt.close()


plansza = Plansza(40, 5000, 3, 20, 3)
for i in range(300):
    plansza.dodaj_rybe()
for i in range(10):
    plansza.dodaj_rekina()
plansza.symuluj()