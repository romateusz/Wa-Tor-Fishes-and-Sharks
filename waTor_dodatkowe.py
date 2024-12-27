import random
import numpy as np
import matplotlib.pyplot as plt

class Organizm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wiek = 1

class Ryba(Organizm):
    '''
    dodano rozmnażanie zależne od wieku:
        gdy wiek < 7 to co czas rozmnażania młodego
        gdy wiek < 14 to czas rozmnażania dorosłego
        gdy wiek >= 14 to już się nie rozmnaża
    i dodano śmierć naturalną:
        gdy wiek == 20 to ginie
    '''
    def __init__(self, x, y, czas_rozmnazania_mlodego, czas_rozmazania_doroslego):
        super().__init__(x, y)
        self.czas_rozmnazania = czas_rozmnazania_mlodego
        self.czas_rozmnazania_doroslego = czas_rozmazania_doroslego

    def czy_rozmnazanie(self):
        if self.wiek > 6 and self.wiek < 14:
            self.czas_rozmnazania = self.czas_rozmnazania_doroslego
        elif self.wiek >= 14:
            return False
        return self.wiek % self.czas_rozmnazania == 0
    
    def czy_umiera(self):
        if self.wiek == 20:
            return True
        else:
            return False
    

class Rekin(Organizm):
    '''
    dodano rozmnażanie zależne od wieku:
        gdy wiek < 20 to co czas rozmnażania młodego
        gdy wiek < 70 to czas rozmnażania dorosłego
        gdy wiek >= 14 to już się nie rozmnaża
    i dodano śmierć naturalną:
        gdy wiek == 80 to ginie
    '''
    def __init__(self, x, y, energia_poczatkowa, czas_rozmnazania_mlodego, czas_rozmazania_doroslego, szansa_na_sukces_polowania):
        super().__init__(x, y)
        self.energia = energia_poczatkowa
        self.czas_rozmnazania = czas_rozmnazania_mlodego
        self.czas_rozmnazania_doroslego = czas_rozmazania_doroslego
        self.szansa_na_sukces_polowania = szansa_na_sukces_polowania

    def czy_umiera(self):
        if self.wiek == 80:
            return True
        else:
            return self.energia <= 0

    def czy_rozmnazanie(self):
        if self.wiek > 20 and self.wiek < 70:
            self.czas_rozmnazania = self.czas_rozmnazania_doroslego
        elif self.wiek >= 70:
            return False
        return self.wiek % self.czas_rozmnazania == 0


class Plansza:
    def __init__(self, rozmiar, max_iter, czas_rozmnazania_ryb_mlodych, czas_rozmnazania_ryb_doroslych, czas_rozmnazania_rekina_mlodego, czas_rozmnazania_rekina_doroslego, energia_rekina, szansa_na_sukces_polowania, co_ile_atak_potwora, rozmiar_potwora):
        self.rozmiar = rozmiar
        self.siatka = [[None for _ in range(rozmiar)] for _ in range(rozmiar)]
        self.pusta_siatka = []
        self.organizmy = []
        for x in range(rozmiar):
            for y in range(rozmiar):
                self.pusta_siatka.append((x,y))
        self.max_iter = max_iter
        self.czas_rozmnazania_ryb_mlodych = czas_rozmnazania_ryb_mlodych
        self.czas_rozmnazania_ryb_doroslych = czas_rozmnazania_ryb_doroslych
        self.czas_rozmnazania_rekina_mlodego = czas_rozmnazania_rekina_mlodego
        self.czas_rozmnazania_rekina_doroslego = czas_rozmnazania_rekina_doroslego
        self.energia_rekina = energia_rekina
        self.szansa_na_sukces_polowania = szansa_na_sukces_polowania
        self.co_ile_atak_potwora = co_ile_atak_potwora
        self.rozmiar_potwora = rozmiar_potwora

    def dodaj_rybe(self):
        x, y = random.sample(self.pusta_siatka, 1)[0]
        self.pusta_siatka.remove((x, y))
        r = Ryba(x, y, self.czas_rozmnazania_ryb_mlodych, self.czas_rozmnazania_ryb_doroslych)
        self.siatka[x][y] = r
        self.organizmy.append(r)

    def dodaj_rekina(self):
        x, y = random.sample(self.pusta_siatka, 1)[0]
        self.pusta_siatka.remove((x, y))
        r = Rekin(x, y, self.energia_rekina, self.czas_rozmnazania_rekina_mlodego, self.czas_rozmnazania_rekina_doroslego, self.szansa_na_sukces_polowania)
        self.siatka[x][y] = r
        self.organizmy.append(r)
    
    def ruch_ryby(self, ryba):
        if ryba.czy_umiera():
            self.organizmy.remove(ryba)
            self.siatka[ryba.x][ryba.y] = None
        else:
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
                    nowa_ryba = Ryba(st_x, st_y, self.czas_rozmnazania_ryb_mlodych, self.czas_rozmnazania_ryb_doroslych)
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
            random.shuffle(ruchy)
            czy_nie_zrobiony_ruch = True

            for x, y in ruchy:
                if isinstance(self.siatka[x][y], Ryba):
                    if random.random() < rekin.szansa_na_sukces_polowania:
                        ryba = self.siatka[x][y]
                        self.organizmy.remove(ryba)
                        self.siatka[rekin.x][rekin.y] = None
                        rekin.x, rekin.y = ryba.x, ryba.y
                        self.siatka[x][y] = rekin
                        czy_nie_zrobiony_ruch = False
                        rekin.energia = self.energia_rekina
                        rekin.szansa_na_sukces_polowania += 0.1
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
                    nowy_rekin = Rekin(st_x, st_y, self.energia_rekina ,self.czas_rozmnazania_rekina_mlodego, self.czas_rozmnazania_rekina_doroslego, self.szansa_na_sukces_polowania)
                    self.siatka[st_x][st_y] = nowy_rekin
                    self.organizmy.append(nowy_rekin)
            rekin.wiek += 1

    def atak_wielkiego_potwora(self):
        x_sr = random.randint(0, self.rozmiar - 1)
        y_sr = random.randint(0, self.rozmiar - 1)
        r = int(self.rozmiar_potwora / 2)

        for x in range(x_sr - r, x_sr + r + 1):
            for y in range(y_sr - r, y_sr + r + 1):
                x_wrapped = x % self.rozmiar
                y_wrapped = y % self.rozmiar
                if ((x - x_sr)**2 + (y - y_sr)**2 <= r**2):
                    if self.siatka[x_wrapped][y_wrapped] is not None:
                        org = self.siatka[x_wrapped][y_wrapped]
                        self.organizmy.remove(org)
                        self.siatka[x_wrapped][y_wrapped] = None

    def symuluj(self):
        tab_ryb, tab_rek = [], []
        for iter in range(1, self.max_iter + 1):
            print(iter)
            if iter % self.co_ile_atak_potwora == 0:
                self.atak_wielkiego_potwora()
            l_ryb, l_rek = 0, 0
            for org in self.organizmy:
                if isinstance(org, Ryba):
                    l_ryb += 1
                else:
                    l_rek +=1 
            tab_ryb.append(l_ryb)
            tab_rek.append(l_rek)

            self.wyswietl_plansze(iter)

            for organizm in self.organizmy:
                if isinstance(organizm, Ryba):
                    self.ruch_ryby(organizm)
                else:
                    self.ruch_rekina(organizm)
        return tab_ryb, tab_rek

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

# tworzenie planszy
plansza = Plansza(rozmiar=200, max_iter=1000, czas_rozmnazania_ryb_mlodych=3,
                 czas_rozmnazania_ryb_doroslych=2, czas_rozmnazania_rekina_mlodego=20,
                 czas_rozmnazania_rekina_doroslego=10, energia_rekina=8, szansa_na_sukces_polowania=0.5,
                 co_ile_atak_potwora=130, rozmiar_potwora=150)
for i in range(7500):
    plansza.dodaj_rybe()
for i in range(250):
    plansza.dodaj_rekina()

# symulacja
tab_ryb, tab_rek = plansza.symuluj()

# rysowanie wykresów
plt.title("ryby i rekiny w czasie")
plt.plot(tab_ryb, color="red", label="ryby")
plt.plot(tab_rek, color="blue", label="rekiny")
plt.legend()
plt.savefig("ryb_i_rek_w_czasie.png")
plt.close()

plt.title("zależność liczby rekinów od ryb")
plt.scatter(tab_ryb, tab_rek)
plt.savefig("rekiny_od_ryb.png")
plt.close()