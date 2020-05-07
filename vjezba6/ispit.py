import json
import sqlite3

class Ispiti(dict):

     def dodaj(self, student, kolegij, ocjena):
          if student not in self:
               self[student] = {}
          self[student][kolegij] = ocjena

     def izbrisi(self, student, kolegij):
          if kolegij in self[student]:
               self[student].pop(kolegij)

     def promijeni(self, student, kolegij, ocjena):
          self[student][kolegij] = ocjena

     def spremi_datoteka(self, datoteka):
          with open(datoteka, 'w') as d:
            for x, kljuc in self.items():
               student=x
               for kolegij in kljuc:
                    podaci="%s \t %s \t %s\n" %(student, kolegij, kljuc[kolegij])
                    d.write(podaci)

     @staticmethod
     def ucitaj_datoteka(datoteka):
          ispit=Ispiti()
          with open(datoteka, 'r') as d:
               for i in range(len(open("ispiti.txt").readlines())):
                    line=d.readline()
                    student=(line.splitlines()[0]).split("\t")
                    ispit.dodaj(student[0],student[1],student[2])
               return ispit

     def spremi_json(self, datoteka):
        with open(datoteka, "w") as d:
            json.dump(self,d)

     @staticmethod
     def ucitaj_json(datoteka):
        with open(datoteka) as d:
            student = json.load(d)
            return student


class IspitiDB():

     def __init__(self, baza):
          self.conn = sqlite3.Connection(baza)
          self.cur = self.conn.cursor()

          self.cur.executescript("""
               DROP TABLE IF EXISTS ispiti;
               DROP TABLE IF EXISTS kolegiji;
               DROP TABLE IF EXISTS studenti;
               CREATE TABLE studenti (
               student_id integer PRIMARY KEY,
               ime_prezime text NOT NULL UNIQUE);
               CREATE TABLE kolegiji (
               kolegij_id integer PRIMARY KEY,
               naziv text NOT NULL UNIQUE);
          CREATE TABLE ispiti (
          student_id integer,
          kolegij_id integer,
          ocjena integer NOT NULL,
          PRIMARY KEY (student_id, kolegij_id),
          FOREIGN KEY (student_id) REFERENCES studenti (student_id),
          FOREIGN KEY (kolegij_id) REFERENCES kolegij (kolegij_id));
          """)

     def vrati_kolegij_id(self, naziv):
          self.cur.execute("""SELECT kolegij_id FROM kolegiji WHERE naziv = ?""", (naziv,))
          row = self.cur.fetchone()
          if row:
               return row[0]

     def dodaj_kolegij(self, naziv):
          self.cur.execute("""INSERT INTO kolegiji (naziv) VALUES (?)""", (naziv, ))
          self.conn.commit()
          return self.cur.lastrowid

     def vrati_student_id(self,ime_prezime):
        self.cur.execute("""SELECT student_id FROM studenti WHERE ime_prezime=?""", (ime_prezime, ))
        row = self.cur.fetchone()
        if row:
            return row[0]
     def vrati_ispit(self,student_id,kolegij_id):
        self.cur.execute("""SELECT * FROM ispiti WHERE student_id=? AND kolegij_id=?""", (student_id, kolegij_id))
        row = self.cur.fetchone()
        if row:
            return row[0]

     def dodaj_student(self, ime_prezime):
        self.cur.execute("""INSERT INTO studenti (ime_prezime) VALUES (?)""",(ime_prezime, ))
        self.conn.commit()
        return self.cur.lastrowid

     def promijeni_student(self, staro_ime, novo_ime):
        if(self.vrati_student_id(staro_ime)):
            self.cur.execute("""UPDATE studenti SET ime_prezime=? WHERE ime_prezime=?""",
                              (novo_ime, staro_ime))
            self.conn.commit()
        else:
            return None

     def izbrisi_student(self, ime_prezime):
        self.cur.execute("DELETE FROM studenti WHERE ime_prezime = ?", (ime_prezime, ))
        self.conn.commit()

     def ispitaj(self,student,kolegij,ocjena=None):
        student_id=self.vrati_student_id(student)
        kolegij_id=self.vrati_kolegij_id(kolegij)
        imaIspit = self.vrati_ispit(student_id,kolegij_id)
        if(ocjena==None):
            self.cur.execute("DELETE FROM ispiti WHERE student_id = ? AND kolegij_id=?",
                               (student_id, kolegij_id))
            self.conn.commit()
        if(student_id==None):
               self.dodaj_student(student)

        if(kolegij_id==None):
               self.dodaj_kolegij(kolegij)
               self.conn.commit()

        if(ocjena and imaIspit!=None):
               self.cur.execute("UPDATE ispiti SET ocjena = ? WHERE student_id = ? AND kolegij_id=?",
                               (ocjena, student_id, kolegij_id))
               self.conn.commit()
        elif(ocjena):
               self.cur.execute("INSERT INTO ispiti (student_id, kolegij_id, ocjena) VALUES (?, ?, ?)",
                               (student_id, kolegij_id, ocjena))
               self.conn.commit()

     def svi_ispiti(self):
          self.cur.execute("""SELECT studenti.ime_prezime, kolegiji.naziv, ocjena FROM ispiti
                            JOIN studenti ON studenti.student_id = ispiti.student_id
                            JOIN kolegiji ON kolegiji.kolegij_id=ispiti.kolegij_id""")

          self.conn.commit()
          lista = self.cur.fetchall()

          ispit = Ispiti()
          for x in lista:
               ispit.dodaj(x[0],x[1],x[2])
          if not len(ispit):
               return None
          return ispit

print("*** TEST datoteka ***")
isp = Ispiti()
isp.dodaj("Ante Antic", "Linearna algebra", 5)
isp.dodaj("Ante Antic", "Programiranje 1", 4)
isp.dodaj("Marija Marijic", "Linearna algebra", 4)
isp.dodaj("Marija Marijic", "Matematicka analiza", 5)
isp.spremi_datoteka("ispiti.txt")
print(open("ispiti.txt").read())
isp = Ispiti.ucitaj_datoteka("ispiti.txt")
print(isp)

print("*** TEST json ***")
isp = Ispiti()
isp.dodaj("Ante Antic", "Linearna algebra", 5)
isp.dodaj("Ante Antic", "Programiranje 1", 4)
isp.dodaj("Marija Marijic", "Linearna algebra", 4)
isp.dodaj("Marija Marijic", "Matematicka analiza", 5)
isp.spremi_json("ispiti.json")
print(open("ispiti.json").read())
isp = Ispiti.ucitaj_json("ispiti.json")
print(isp)

print('*** TEST SQLite studenti ***')
db = IspitiDB("ispiti.sqlite")
print(db.cur.execute("SELECT * FROM studenti").fetchall())
db.dodaj_student("Ante Antic")
db.dodaj_student("Ana Anic")
db.dodaj_student("Pero Peric")
print(db.cur.execute("SELECT * FROM studenti").fetchall())
print(db.vrati_student_id("Pero Peric"))
print(db.vrati_student_id("Marija Marijic"))
db.izbrisi_student("Pero Peric")
db.promijeni_student("Ana Anic", "Marija Marijic")
print(db.cur.execute("SELECT * FROM studenti").fetchall())

print('*** TEST SQLite ispiti ***')
db = IspitiDB("ispiti.sqlite")
db.dodaj_student("Ante Antic")
db.dodaj_student("Marija Marijic")
db.dodaj_kolegij("Linearna algebra")
db.ispitaj("Ante Antic", "Linearna algebra", 5)
print(db.svi_ispiti())
db.ispitaj("Ante Antic", "Linearna algebra", 4)
print(db.svi_ispiti())
db.ispitaj("Ante Antic", "Linearna algebra")
print(db.svi_ispiti())
db.ispitaj("Ante Antic", "Linearna algebra", 5)
db.ispitaj("Marija Marijic", "Programiranje 1", 5)
db.ispitaj("Marija Marijic", "Matematicka analiza", 4)
print(db.svi_ispiti())
