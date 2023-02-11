from linker.linker import *


def menu_neregistrovan():

    menu_dict = {
        '1': prijava_na_sistem,
        '2': registracija_kupca,
        '3': prikaz_nerealizovanih_letova,
        '4': trazenje_letova,
        '5': prikaz_10_najjeftinijih,
        '6': fleksibilna_pretraga,
        'x': izlaz
    }

    while True:
        clear()
        print("=" * 50)
        print("Glavni meni aplikacije za neregistrovane")
        print("=" * 50)
        
        print("Ponuđene opcije:")

        print("1. Prijava na sistem")
        print("2. Registracija")
        print("3. Pregled nerealizovanih letova")
        print("4. Pretraga letova")
        print("5. 10 najjeftinijih letova")
        print("6. Fleksibilna pretraga")
        print("x. Izlaz")

        user_input = input(">>")

        if user_input in menu_dict:
            menu_dict[user_input]()

        else:
            print("Odabrali ste nepostojeću opciju")
            input("Pritisnite enter za nazad")



if __name__ == '__main__':
    menu_neregistrovan()
