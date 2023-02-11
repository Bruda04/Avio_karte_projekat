# from korisnici.korisnici import ucitaj_korisnike_iz_fajla
# print(ucitaj_korisnike_iz_fajla("korisnici.csv", ","))
# from korisnici.korisnici import ucitaj_korisnike_iz_fajla, sacuvaj_korisnike, login, kreiraj_korisnika

# print(ucitaj_korisnike_iz_fajla("korisnici.csv", ","))


# from korisnici.korisnici import login, logout, ucitaj_korisnike_iz_fajla, ko_je_ulogovan
# import korisnici.korisnici
# print(ko_je_ulogovan())

# login(ucitaj_korisnike_iz_fajla("korisnici.csv", ","), "lluka", "password")

# print(ko_je_ulogovan())

# logout(ko_je_ulogovan())

# print(ko_je_ulogovan())

# from datetime import datetime

# sad  = datetime.now()
# if isinstance(sad, datetime):
#     print("da")
# print()


# from izvestaji.izvestaji import izvestaj_prodatih_karata_za_dan_prodaje

# dictvreme = datetime.datetime(2020, 10, 11, 14, 30, 18)
# datum =  datetime.datetime(2020, 10, 11, 14, 30, 18)
# vreme = '10:37'

# print(dictvreme, datum, vreme)


# sad =datetime(2022,12,15,12,12,12)

# datum = datetime.now()

# diff = datum - sad

# print(diff.days)

# dani = [0,3,5]
# for i in range(diff.days):
#     dan = (sad + timedelta(days=i)).weekday()
#     if dan in dani:
#         print(i)


# from konkretni_letovi.konkretni_letovi import ucitaj_konkretan_let, sacuvaj_kokretan_let, kreiranje_konkretnog_leta
# from letovi.letovi import ucitaj_letove_iz_fajla

# svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
# konkretni = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
# for let in svi_letovi:
#     kreiranje_konkretnog_leta(konkretni, svi_letovi[let])

# sacuvaj_kokretan_let("konkretni_letovi.csv", "|", konkretni)

from menu.neregistrovan import menu_neregistrovan
import os
from linker.linker import clear
os.system('color a')
clear()
menu_neregistrovan()

