# # This is a sample Python script.

# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# # See PyCharm help at https://www.jetbrains.com/help/pycharm/


from korisnici.korisnici import kreiraj_korisnika, ucitaj_korisnike_iz_fajla, sacuvaj_korisnike, login

#print(ucitaj_korisnike_iz_fajla("korisnici.csv", ","))
# sacuvaj_korisnike("korisnici.csv", ",", kreiraj_korisnika(ucitaj_korisnike_iz_fajla("korisnici.csv", ","),False, "korisnik",None, "anaa","123","ana","krunic","anak@mail.com", "123456789", "nase", "1234132312", "z"))
sacuvaj_korisnike("korisnici.csv", ",", kreiraj_korisnika(ucitaj_korisnike_iz_fajla("korisnici.csv", ","),False, "korisnik","anaa", "kruicana","123","ana","krunic","kana@mail.com", "123456789", "marsovac", "1234132312", "z"))
#print(login(ucitaj_korisnike_iz_fajla("korisnici.csv",","),"mmatijaa","matija111"))
#print(ucitaj_korisnike_iz_fajla("korisnici.csv", ","))
#sacuvaj_korisnike("korisnici.csv", ",",{"lluka": {"korisnicko_ime":"lluka", "lozinka":"123", "ime":"lukaaaa", "prezime":"bradic", "uloga":"menadzer","email":"bradic@", "pasos":"123412", "drzavljanstvo":"moje", "telefon":"124", "pol":"M"}})

#print(kreiraj_korisnika(ucitaj_korisnike_iz_fajla("korisnici.csv", ","),False,"menadzer","mmatijaaa","123","jaja","titi"))

