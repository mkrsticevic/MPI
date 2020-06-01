from random import *

class Polje():

    def __init__(self, velicina, broj_mina):
        self.__velicina = velicina
        self.__broj_mina = broj_mina
        self.__kvadrati = [[Kvadrat() for col in range(velicina)] for row in range(velicina)]

        for mine in range(broj_mina):
            random_num = randrange(velicina ** 2)
            col = random_num // velicina
            row = random_num % velicina

            self.__kvadrati[col][row] = Kvadrat(-1)

        for col in range(velicina):
            for row in range(velicina):
                if self.__kvadrati[col][row].jeMina:
                    continue

                num_of_mines = 0

                for counter in [-1, 0, 1]:
                    row1 = self.check_for_a_mine(col - 1, row + counter)
                    row2 = self.check_for_a_mine(col, row + counter)
                    row3 = self.check_for_a_mine(col + 1, row + counter)

                    if (row1 == -1):
                        num_of_mines += 1
                    if (row2 == -1):
                        num_of_mines += 1
                    if (row3 == -1):
                        num_of_mines += 1

                self.__kvadrati[col][row] = Kvadrat(num_of_mines)

    def check_for_a_mine(self, x, y):
        if x >= 0 and y >= 0 and x < self.__velicina and y < self.__velicina:
            if self.__kvadrati[x][y].jeMina:
                return -1
            else:
                return 0

    def __str__(self):
        output = "   1 2 3 4 5\n  -----------"
        for cols in range(self.__velicina):
            output += "\n" + str(cols + 1) + "| "
            for rows in range(self.__velicina):
                output += str(self.__kvadrati[cols][rows]) + " "
            output +="|"

        output += "\n  ----------"

        return output

class Kvadrat():

    def __init__(self, broj = 0):
        self.__broj = broj
        self.__otkriven = False
        self.__oznaka = False

    def otkrij(self):
        if self.__otkriven == False:
            self.__otkriven = True

    def oznaci(self):
        if self.__oznaka == False:
            self.__oznaka = True
        else:
            self.__oznaka = False

    @property
    def jeMina(self):
        if self.__broj == -1:
            return True
        return False

    @property
    def jeBroj(self):
        if self.__broj > 0:
            return True
        return False

    @property
    def broj(self):
        return self.__broj

    @property
    def jePrazan(self):
        if self.__broj == 0:
            return True
        return False
    def __str__(self):
        if self.__otkriven == False:
            return "."
        elif self.__oznaka == True:
            return "?"
        elif self.__otkriven == True and self.__broj == -1:
            return "x"
        elif self.__otkriven == True and self.__broj > 0:
            return str(self.__broj)
        elif self.__otkriven == True and self.__broj == 0:
            return " "

class PrikazIgre():

    def izaberiTezinu(self, tezina list):
        tezine = {}

        print("Izaberi tezinu:")

        for counter in range(len(tezina)):
            tezine[str(counter + 1)] = tezina[counter]

            print(counter + 1, ". velicina ", tezina[counter][0], ", broj mina ",tezina[counter][1], sep = "")

        while True:
            odabranaTezina = str(input("\nOdaberite jednu od navedenih tezina: "))


            if odabranaTezina in tezine:
                print("Odabrana je te??ina", odabranaTezina)
                return odabranaTezina
            else:
                print("*" * 10, "NEVALJANA TE??INA", "*" * 10)


    def prikaziPolje(self, polje: Polje):
            print(polje)
    def unesiAkciju(self, velicina):
        print("\n", "*" * 10, "PRAVILO UNOSA", "*" * 10 ,"\nAko ??elite otkriti polje unesite koordinate polja (npr [2 3] ili [2,3]) kojeg ??elite otkriti\nAko ??elite ozna??iti polje ispred unosa koordinata dodajte znak '?' (npr [?2 3], [? 2,3] ili [? 2 3])")
        while True:
            koordinata = input("Unesite koordinate: ")
            koordinateTrimed = ""
            operacija = ""

            if "?" in koordinata:
                operacija = "oznaci"
                koordinateTrimed = koordinata.replace("?", "").strip()
            else:
                operacija = "otkrij"
                koordinateTrimed = koordinata

            if "," in koordinata:
                koordinateTrimed = koordinateTrimed.split(",")
            else:
                koordinateTrimed = koordinateTrimed.split(" ")

            try:
                koordinateTrimed = [int(koordinateTrimed[0]), int(koordinateTrimed[1])]
            except:
                continue

            if (koordinateTrimed[0] > 0 and koordinateTrimed[0] <= velicina) and (koordinateTrimed[1] > 0 and koordinateTrimed[1] <= velicina):
                return (operacija, koordinateTrimed[0], koordinateTrimed[1])

print('*** test 1 ***')
pi = PrikazIgre()
print(pi.izaberiTezinu([(9,8), (15,14), (20,18), (30,30)]))

print('*** test 2 ***')
p = Polje(5,2)
pi = PrikazIgre()
pi.prikaziPolje(p)

pi = PrikazIgre()
print(pi.unesiAkciju(9))
print(pi.unesiAkciju(3))
