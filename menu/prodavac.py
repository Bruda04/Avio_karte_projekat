from linker.linker import *
from korisnici.korisnici import ko_je_ulogovan


def menu_prodavac():

    menu_dict = {
        '1': prikaz_nerealizovanih_letova,
        '2': trazenje_letova,
        '3': prikaz_10_najjeftinijih,
        '4': fleksibilna_pretraga,

        '5': prodaj_kartu,
        '6': prijava_na_let_prodavac,
        '7': izmeni_kartu,
        '8': oznaci_za_brisanje_karata,
        '9': prikaz_pretraga_prodatih_karata,

        '10': odjava,
        'x': izlaz
    }

    while True:
        clear()
        print("=" * 50)
        print("Glavni meni aplikacije za prodavce")
        print("=" * 50)
        if ko_je_ulogovan():
            korisnik = ko_je_ulogovan()["korisnicko_ime"]
            print(f"Ulogovan je prodavac: {korisnik}!")
            print("=" * 50)
        print("Ponuđene opcije:")

        print("1. Pregled nerealizovanih letova")
        print("2. Pretraga letova")
        print("3. 10 najjeftinijih letova")
        print("4. Fleksibilna pretraga")

        print("5. Prodaja karata")
        print("6. Prijava na let")
        print("7. Izmena karte")
        print("8. Brisanje karte")
        print("9. Pretraga prodatih karata")
    
        print("10. Odjava")
        print("x. Izlaz")

        user_input = input(">>")

        if user_input in menu_dict:
            menu_dict[user_input]()

        else:
            print("Odabrali ste nepostojeću opciju")
            input("Pritisnite enter za nazad")

if __name__ == '__main__':
    menu_prodavac()
