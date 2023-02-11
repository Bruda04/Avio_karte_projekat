from linker.linker import *
from korisnici.korisnici import ko_je_ulogovan


def menu_menadzer():

    menu_dict = {
        '1': prikaz_nerealizovanih_letova,
        '2': trazenje_letova,
        '3': prikaz_10_najjeftinijih,
        '4': fleksibilna_pretraga,

        '5': prikaz_pretraga_prodatih_karata,
        '6': registrovanje_novih_prodavaca,
        '7': kreiraj_let,
        '8': izmeni_let,
        '9': zapravo_obrisi_kartu,
        '10': generisi_izvestaje,

        '11': odjava,
        'x': izlaz
    }

    while True:
        clear()
        print("=" * 50)
        print("Glavni meni aplikacije za menadzere")
        print("=" * 50)
        if ko_je_ulogovan():
            korisnik = ko_je_ulogovan()["korisnicko_ime"]
            print(f"Ulogovan je menadzer: {korisnik}!")
            print("=" * 50)
        
        print("Ponuđene opcije:")
        print("1. Pregled nerealizovanih letova")
        print("2. Pretraga letova")
        print("3. 10 najjeftinijih letova")
        print("4. Fleksibilna pretraga")

        print("5. Pretraga prodatih karata")
        print("6. Registracija novih prodavaca")
        print("7. Kreiranje letova")
        print("8. Izmena letova")
        print("9. Brisanje karata")
        print("10. Izvestaji")
    
        print("11. Odjava")
        print("x. Izlaz")
        user_input = input(">>")

        if user_input in menu_dict:
            menu_dict[user_input]()

        else:
            print("Odabrali ste nepostojeću opciju")
            input("Pritisnite enter za nazad")

if __name__ == '__main__':
    menu_menadzer()
