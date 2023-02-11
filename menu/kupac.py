from linker.linker import *
from korisnici.korisnici import ko_je_ulogovan


def menu_kupac():

    menu_dict = {
        '1': prikaz_nerealizovanih_letova,
        '2': trazenje_letova,
        '3': prikaz_10_najjeftinijih,
        '4': fleksibilna_pretraga,

        '5': kupi_kartu,
        '6': prikaz_nerealizovanih_karata,
        '7': prijava_na_let,
        
        '8': odjava,
        'x': izlaz
    }

    while True:
        clear()
        print("=" * 50)
        print("Glavni meni aplikacije za kupce")
        print("=" * 50)
        if ko_je_ulogovan():
            korisnik = ko_je_ulogovan()["korisnicko_ime"]
            print(f"Ulogovan je kupac: {korisnik}!")
            print("=" * 50)
        print("Ponuđene opcije:")

        print("1. Pregled nerealizovanih letova")
        print("2. Pretraga letova")
        print("3. 10 najjeftinijih letova")
        print("4. Fleksibilna pretraga")

        print("5. Kupovina karata")
        print("6. Pregled nerealizovanih karata")
        print("7. Prijava na let")
    
        print("8. Odjava")
        print("x. Izlaz")

        user_input = input(">>")

        if user_input in menu_dict:
            menu_dict[user_input]()

        else:
            print("Odabrali ste nepostojeću opciju")
            input("Pritisnite enter za nazad")


if __name__ == '__main__':
    menu_kupac()
