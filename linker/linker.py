import os
import platform
from datetime import datetime
import common.konstante 
from korisnici.korisnici import login, ucitaj_korisnike_iz_fajla, ko_je_ulogovan, sacuvaj_korisnike, logout, kreiraj_korisnika
from letovi.letovi import povezani_letovi,trazenje_10_najjeftinijih_letova, ucitaj_letove_iz_fajla, pretraga_letova, pregled_nerealizoivanih_letova, fleksibilni_polasci, kreiranje_letova,sacuvaj_letove, izmena_letova, checkin, podesi_matricu_zauzetosti
from konkretni_letovi.konkretni_letovi import ucitaj_konkretan_let, sacuvaj_kokretan_let, kreiranje_konkretnog_leta
from karte.karte import ucitaj_karte_iz_fajla, pregled_nerealizovanaih_karata, brisanje_karte, sacuvaj_karte, pretraga_prodatih_karata, izmena_karte, kupovina_karte
from model_aviona.model_aviona import ucitaj_modele_aviona
from izvestaji.izvestaji import *


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Darwin":
        os.system("clear")

def izlaz():
    clear()
    os.system("color 7")
    exit()

def prijava_na_sistem():

    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prijava na sistem")
            print("=" * 50)
            ime = input("Unesite korisnicko ime: >>")
            sifra = input("Unesite lozinku: >>")

            login(ucitaj_korisnike_iz_fajla("korisnici.csv", "|"), ime, sifra)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni podaci!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return 
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")

    uloga_korisnika = ko_je_ulogovan()["uloga"]
    if uloga_korisnika == common.konstante.ULOGA_KORISNIK:
        from menu.kupac import menu_kupac
        menu_kupac()
    if uloga_korisnika == common.konstante.ULOGA_ADMIN:
        from menu.menadzer import menu_menadzer
        menu_menadzer()
    if uloga_korisnika == common.konstante.ULOGA_PRODAVAC:
        from menu.prodavac import menu_prodavac
        menu_prodavac()

def registracija_kupca():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Registracija")
            print("=" * 50)
            korisnicko_ime = input("Unesite korisnicko ime: >>")
            lozinka = input("Unesite lozinku: >>")
            ime = input("Unesite ime: >>")
            prezime = input("Unesite prezime: >>")
            email = input("Unesite email: >>")
            pasos = input("Unesite pasos (opciono): >>")
            drzavljanstvo = input("Unesite drzavljanstvo (opciono): >>")
            telefon = input("Unesite telefon: >>")
            pol = input("Unesite pol (M/F) (opciono): >>")

            svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")

            novi_korisnici = kreiraj_korisnika(svi_korisnici, False, common.konstante.ULOGA_KORISNIK, "", korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
            sacuvaj_korisnike("korisnici.csv", "|", novi_korisnici)

            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    input("Uspesno ste se registrovali!\nPritisnite enter za nazad")

def prikaz_nerealizovanih_letova():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prikaz letova koji nisu realizovani")
            print("=" * 50)
        
            # konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            
            letovi = pregled_nerealizoivanih_letova(svi_letovi)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    print ("{:<10} {:<20} {:<20}".format("Broj leta", "Polazak", "Dolazak"))
    print("=" * 60)
    for let in letovi:
        datum_pocetka_operativnosti = let["datum_pocetka_operativnosti"].strftime("%d.%m.%y. %H:%M")
        datum_kraja_operativnosti = let["datum_kraja_operativnosti"].strftime("%d.%m.%y. %H:%M")

        print ("{:<10} {:<20} {:<20}".format(let["broj_leta"], datum_pocetka_operativnosti, datum_kraja_operativnosti))
    print("=" * 60)
    input("Pritisnite bilo koji taster za nazad")

def trazenje_letova():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Pretraga letova")
            print("=" * 50)
            polaziste = input("Unesite polaziste: >>")
            odrediste = input("Unesite odrediste: >>")
            datum_polaska = input("Unesite datum polaska(dd.mm.yyyy.): >>")
            if  not datum_polaska:
                pass
            else:
                datum_polaska = datetime.strptime(datum_polaska, "%d.%m.%Y.")
            
            datum_dolaska = input("Unesite datum dolaska(dd.mm.yyyy.): >>")
            if not datum_dolaska:
                pass
            else:
                datum_dolaska = datetime.strptime(datum_dolaska, "%d.%m.%Y.")
            vreme_poletanja = input("Unesite vreme poletanja(hh:mm): >>")
            vreme_sletanja = input("Unesite vreme sletanja(hh:mm): >>")
            prevoznik = input("Unesite prevoznika: >>")

            konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            
            letovi = pretraga_letova(svi_letovi, konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    print ("{:<10} {:<10} {:<20} {:<20}".format("Broj leta", "Sifra", "Polazak", "Dolazak"))
    print("=" * 60)
    for let in letovi:
        datum_i_vreme_polaska = let["datum_i_vreme_polaska"].strftime("%d.%m.%y. %H:%M")
        datum_i_vreme_dolaska = let["datum_i_vreme_dolaska"].strftime("%d.%m.%y. %H:%M")
        print ("{:<10} {:<10} {:<20} {:<20}".format(let["broj_leta"], let["sifra"], datum_i_vreme_polaska, datum_i_vreme_dolaska))
    print("=" * 60)
    input("Pritisnite bilo koji taster za nazad")

def prikaz_10_najjeftinijih():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Pretraga 10 najjeftinijih letova")
            print("=" * 50)
            polaziste = input("Unesite polaziste: >>")
            odrediste = input("Unesite odrediste: >>")

            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            letovi = trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    print ("{:<20} {:<20}".format("Broj leta", "Cena"))
    print("=" * 50)
    for let in letovi:
        broj_leta = let["broj_leta"]
        cena = let["cena"]
        print ("{:<20} {:<20}".format(broj_leta, cena))
    print("=" * 50)
    input("Pritisnite bilo koji taster za nazad")

def fleksibilna_pretraga():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Pretraga letova")
            print("=" * 50)
            polaziste = input("Unesite polaziste: >>")
            odrediste = input("Unesite odrediste: >>")
            datum_polaska = input("Unesite datum polaska(dd.mm.yyyy.): >>")
            if not datum_polaska:
                pass
            else:
                datum_polaska = datetime.strptime(datum_polaska, "%d.%m.%Y.")

            datum_dolaska = input("Unesite datum dolaska(dd.mm.yyyy.): >>")
            if not datum_dolaska:
                pass
            else:
                datum_dolaska = datetime.strptime(datum_dolaska, "%d.%m.%Y.")

            fleksibilo = input("Unesite broj fleksibilnih dana: >>")

            if not fleksibilo.isdecimal():
                raise Exception("fleksiblinost nije broj")
            else:
                fleksibilo = int(fleksibilo)

            konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            
            letovi = fleksibilni_polasci(svi_letovi, konkretni_letovi, polaziste, odrediste, datum_dolaska, fleksibilo, datum_dolaska)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    print ("{:<10} {:<10} {:<20} {:<20}".format("Broj leta", "Sifra", "Polazak", "Dolazak"))
    print("=" * 60)
    for let in letovi:
        datum_i_vreme_polaska = let["datum_i_vreme_polaska"].strftime("%d.%m.%y. %H:%M")
        datum_i_vreme_dolaska = let["datum_i_vreme_dolaska"].strftime("%d.%m.%y. %H:%M")
        print ("{:<10} {:<10} {:<20} {:<20}".format(let["broj_leta"], let["sifra"], datum_i_vreme_polaska, datum_i_vreme_dolaska))
    print("=" * 60)
    input("Pritisnite bilo koji taster za nazad")

def odjava():
    from menu.neregistrovan import menu_neregistrovan
    logout(ko_je_ulogovan())
    menu_neregistrovan()

def kupi_kartu():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Kupovina karte")
            print("=" * 50)

            trazenje_letova()
            korisnik = ko_je_ulogovan()
            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            broj_konkretnog_leta = int(input("Unesite sifru konkretnog leta: >>"))
            if broj_konkretnog_leta not in svi_konkretni_letovi:
                raise Exception("Uneli ste nepostojeci broj konkretnog leta")

            slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

            ima_mesta = False

            for red in slobodna_mesta:      #provera da li ima mesta
                if ima_mesta:
                    break
                for sediste in red:
                    if not sediste:
                        ima_mesta = True
                        break
                
            if not ima_mesta:
                raise Exception("Na letu nema slobodnih mesta")
            

            putnici = []
            user_input = None
            while user_input != "1" and user_input != "2":
                clear()
                print("Da li kartu kupujete za sebe ili drugog?")
                print("1. Za sebe")
                print("2. Za drugu osobu")
                user_input = input(">>")
                if user_input == "1":
                    putnici.append(korisnik)
                    continue
                elif user_input == "2":
                    ime_drugog = input("Unesite ime osobe: >>")
                    prezime_drugog = input("Unesite prezime osobe: >>")
                    pasos_drugog = input("Unesite broj pasosa osobe(opciono): >>")
                    drzavljanstvo_drugog = input("Unesite drzavljanstvo osobe(opciono): >>")
                    pol_drugog = input("Unesite pol osobe(opciono): >>")
                    drugi_recnik = {
                        "ime": ime_drugog,
                        "prezime": prezime_drugog,
                        "korisnicko_ime": ime_drugog+prezime_drugog
                        }

                    drugi_recnik["pasos"] = pasos_drugog
                    drugi_recnik["drzavljanstvo"] = drzavljanstvo_drugog
                    drugi_recnik["pol"] = pol_drugog
                    putnici.append(drugi_recnik)
                    continue
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")

            
            potvrda = None
            while potvrda != "da" and potvrda != "ne":
                print("Da li zelite da kupite sledecu kartu(da/ne):")
                print(f"Broj leta: {broj_konkretnog_leta}")
                print("Za putnike:")
                for putnik in putnici:
                    print(f'    {putnik["ime"]} {putnik["prezime"]}')
                potvrda = input(">>")
                if potvrda == "da":
                    continue
                elif potvrda == "ne":
                    raise Exception("Odustali ste od kupovine karte")
                else:
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")



            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            karta, sve_karte_nove = kupovina_karte(
                            sve_karte,
                            svi_konkretni_letovi,
                            broj_konkretnog_leta,
                            putnici,
                            slobodna_mesta,
                            korisnik
                           )
            sacuvaj_karte(sve_karte_nove, "karte.csv", "|")
            
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    
    while True:
        clear()
        print("Uspesno ste kupili kartu!")
        print("=" * 50)
        print("Izaberite jednu od opcija:")
        print("1. Kupite kartu za povezani let")
        print("2. Kupite kartu za saputnika")
        print("b. Zavrsite sa kupovinom")
        opcija = input(">>")
        if opcija == "1":
            gotovo = False
            while not gotovo:
                try:
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    povezani_letovi_opcije = povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[broj_konkretnog_leta])
                    
                    print ("{:<10} {:<10} {:<20} {:<20}".format("Broj leta", "Sifra", "Polazak", "Dolazak"))
                    print("=" * 60)
                    for povezani_let in povezani_letovi_opcije:
                        datum_i_vreme_polaska = povezani_let["datum_i_vreme_polaska"].strftime("%d.%m.%y. %H:%M")
                        datum_i_vreme_dolaska = povezani_let["datum_i_vreme_dolaska"].strftime("%d.%m.%y. %H:%M")
                        print ("{:<10} {:<10} {:<20} {:<20}".format(povezani_let["broj_leta"], povezani_let["sifra"], datum_i_vreme_polaska, datum_i_vreme_dolaska))
                    print("=" * 60)

                    broj_konkretnog_leta = int(input("Unesite sifru konkretnog leta: >>"))
                    valja = False
                    for mogucnosti in povezani_letovi_opcije:
                        if mogucnosti["sifra"] == broj_konkretnog_leta:
                            valja = True
                            break
                    if not valja:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")

                    slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    ima_mesta = False

                    for red in slobodna_mesta:      #provera da li ima mesta
                        if ima_mesta:
                            break
                        for sediste in red:
                            if not sediste:
                                ima_mesta = True
                                break
                        
                    if not ima_mesta:
                        raise Exception("Na letu nema slobodnih mesta")
                    

                    putnici = []
                    
                    putnici.append(korisnik)
                    

                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da kupite sledecu kartu(da/ne):")
                        print(f"Broj leta: {broj_konkretnog_leta}")
                        print("Za putnike:")
                        for putnik in putnici:
                            print(f'    {putnik["ime"]} {putnik["prezime"]}')
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            raise Exception("Odustali ste od kupovine karte")
                        else:
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")



                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    karta, sve_karte_nove = kupovina_karte(
                                    sve_karte,
                                    svi_konkretni_letovi,
                                    broj_konkretnog_leta,
                                    putnici,
                                    slobodna_mesta,
                                    korisnik
                                )
                    sacuvaj_karte(sve_karte_nove, "karte.csv", "|")
                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da kupite jos karata za povezane letove(da/ne):")
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            gotovo = True
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
        
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")


        elif opcija == "2":
            kraj = False
            while not kraj:
                try:
                    clear()
                    print("=" * 50)
                    print("Kupovina karte")
                    print("=" * 50)

                    korisnik = ko_je_ulogovan()
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    if broj_konkretnog_leta not in svi_konkretni_letovi:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")

                    slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    ima_mesta = False

                    for red in slobodna_mesta:      #provera da li ima mesta
                        if ima_mesta:
                            break
                        for sediste in red:
                            if not sediste:
                                ima_mesta = True
                                break
                        
                    if not ima_mesta:
                        raise Exception("Na letu nema slobodnih mesta")
                    

                    putnici = []
                    
                    ime_saputnika = input("Unesite ime osobe: >>")
                    prezime_saputnika = input("Unesite prezime osobe: >>")
                    pasos_saputnika = input("Unesite broj pasosa osobe(opciono): >>")
                    drzavljanstvo_saputnika = input("Unesite drzavljanstvo osobe(opciono): >>")
                    pol_saputnika = input("Unesite pol osobe(opciono): >>")
                    drugi_recnik = {
                        "ime": ime_saputnika,
                        "prezime": prezime_saputnika,
                        "korisnicko_ime": ime_saputnika+prezime_saputnika
                        }
                    if pasos_saputnika:
                        drugi_recnik["pasos"] = pasos_saputnika
                    if drzavljanstvo_saputnika:
                        drugi_recnik["drzavljanstvo"] = drzavljanstvo_saputnika
                    if pol_saputnika:
                        drugi_recnik["pol"] = pol_saputnika
                    putnici.append(drugi_recnik)
                    
                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da dodate saputnika(da/ne):")
                        print(f"Broj leta: {broj_konkretnog_leta}")
                        print("Za putnike:")
                        for putnik in putnici:
                            print(f'    {putnik["ime"]} {putnik["prezime"]}')
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            raise Exception("Odustali ste od kupovine karte")
                        else:
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")



                    sve_karte_update_putnika = ucitaj_karte_iz_fajla("karte.csv", "|")
                    sve_karte_update_putnika[karta["broj_karte"]]["putnici"].extend(putnici)
                    sacuvaj_karte(sve_karte_update_putnika, "karte.csv", "|")
                    
                    jos = None
                    while jos != "da" and jos != "ne":
                        print("Da li zelite da kupite jos karata za saputnike(da/ne):")
                        jos = input(">>")
                        if jos == "da":
                            continue
                        elif jos == "ne":
                            kraj = True
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
                    
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
            
        elif opcija == "b":
            clear()
            return
        else:
            clear()
            print("uneli ste nepostojecu opciju")
            input("Pritisnite enter za nazad")

def prikaz_nerealizovanih_karata():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prikaz karata koje nisu realizovane")
            print("=" * 50)
        
            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            
            karte = pregled_nerealizovanaih_karata(ko_je_ulogovan(), list(sve_karte.values()))

            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    #print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
    print("{:<15} {:<20} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac"))
    print("=" * 70)
    for karta in karte:
        #datum_prodaje = karta["datum_prodaje"].strftime("%d.%m.%y.")
        #print ("{:<15} {:<20} {:<15} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"], datum_prodaje))
        print ("{:<15} {:<20} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"]["ime"] + " " + karta["kupac"]["prezime"]))
    print("=" * 70)
    input("Pritisnite bilo koji taster za nazad")

def prijava_na_let():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prijava na let")
            print("=" * 50)

            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            korisnik = ko_je_ulogovan()
            prikaz_pretraga_prodatih_karata(korisnik["korisnicko_ime"])

            broj_karte = int(input("Unesite broj karte: >>"))
            if broj_karte not in sve_karte:
                raise Exception("Uneli ste nepostojeci broj karte")

            korisnicka_ime_putnika = []
            putnici = sve_karte[broj_karte]["putnici"]
            for putnik in putnici:
                korisnicka_ime_putnika.append(putnik["korisnicko_ime"])
            if korisnik["korisnicko_ime"] not in korisnicka_ime_putnika:
                raise Exception("Niste uneli validnu kartu")

            if not korisnik["pasos"]:
                pasos = input("Unesite broj pasosa: >>")
            else:
                pasos = korisnik["pasos"]
            if not korisnik["drzavljanstvo"]:
                drzavljanstvo = input("Unesite drzavljanstvo: >>")
            else:
                drzavljanstvo = korisnik["drzavljanstvo"]
            if not korisnik["pol"]:
                pol = input("Unesite pol: >>")
            else:
                pol = korisnik["pol"]

            korisnik["pasos"] = pasos
            korisnik["drzavljanstvo"] = drzavljanstvo
            korisnik["pol"] = pol

            svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
            update = kreiraj_korisnika(svi_korisnici, True, 
                                       korisnik["uloga"],
                                       korisnik["korisnicko_ime"],
                                       korisnik["korisnicko_ime"],
                                       korisnik["lozinka"],
                                       korisnik["ime"],
                                       korisnik["prezime"],
                                       korisnik["email"],
                                       korisnik["pasos"],
                                       korisnik["drzavljanstvo"],
                                       korisnik["telefon"],
                                       korisnik["pol"],
                                       )
            sacuvaj_korisnike("korisnici.csv", "|", update)

            if not korisnik["pasos"]:
                raise Exception("Morate uneti broj pasosa da biste se prijavili na let")

            if not korisnik["drzavljanstvo"]:
                raise Exception("Morate uneti drzavljanstvo da biste se prijavili na let")

            if not korisnik["pol"]:
                raise Exception("Morate uneti pol da biste se prijavili na let")


            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            

            broj_konkretnog_leta = sve_karte[broj_karte]["sifra_konkretnog_leta"]
            broj_leta_sa_karte = svi_konkretni_letovi[broj_konkretnog_leta]["broj_leta"]
            model = svi_letovi[broj_leta_sa_karte]["model"]

            broj_redova = model["broj_redova"]
            sedista = model["pozicije_sedista"]

            matrica = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

            print("=" * 50)
            for i in range(broj_redova):
                red = matrica[i]
                stampa = []
                for j in range(len(sedista)):
                    if red[j]:
                        stampa.append("X")
                    if not red[j]:
                        stampa.append(sedista[j])
                
                print(f"{i+1}.  {' '.join(stampa)}")
            print("=" * 50)

            unos_sediste = input("Unesite zeljeno sediste (A1): >>")

            if not unos_sediste[0].isalpha() or not unos_sediste[1:].isdecimal():
                raise Exception("Niste uneli validan format sedista")
            if unos_sediste[0].upper() not in sedista:
                raise Exception("Uneli ste nepostojece slovo")
            if int(unos_sediste[1:]) > broj_redova or int(unos_sediste[1:]) <= 0:
                raise Exception("Uneli ste los broj reda")
            
            odabrani_red = int(unos_sediste[1:])
            odabrana_pozicija = unos_sediste[0].upper()
            
            novi_konkretni_let, nova_karta = checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[broj_konkretnog_leta], odabrani_red, odabrana_pozicija)

            svi_konkretni_letovi_novi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            
            svi_konkretni_letovi_novi[novi_konkretni_let["sifra"]] = novi_konkretni_let
            sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi_novi)

            sve_karte_nove = ucitaj_karte_iz_fajla("karte.csv", "|")
            putnici_update = nova_karta["putnici"]
            for putnik in range(len(putnici_update)):
                if putnici_update[putnik]["korisnicko_ime"] == korisnik["korisnicko_ime"]:
                    putnici_update[putnik]["pasos"] = pasos
                    putnici_update[putnik]["drzavljanstvo"] = drzavljanstvo
                    putnici_update[putnik]["pol"] = pol

            nova_karta["kupac"] = ko_je_ulogovan()    
            nova_karta["putnici"] = putnici_update

            sve_karte_nove[nova_karta["broj_karte"]] = nova_karta
            sacuvaj_karte(sve_karte_nove, "karte.csv", "|")

            
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()


    while True:
        clear()
        print("Uspesno ste se prijavili na let!")
        print("=" * 50)
        print("Izaberite jednu od opcija:")
        print("1. Prijavite se na povezani let")
        print("b. Zavrsite sa prijavnom na letove")
        opcija = input(">>")
        if opcija == "1":
            gotovo = False
            while not gotovo:
                try:
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    povezani_letovi_opcije = povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[broj_konkretnog_leta])

                    korisnikove_karte = pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi, "","","" ,"" , korisnik["korisnicko_ime"])
                    karte_sa_povezanim_letom = []

                    for karta in korisnikove_karte:
                        for povezani_let in povezani_letovi_opcije:
                            if karta["sifra_konkretnog_leta"] == povezani_let["sifra"]:
                                karte_sa_povezanim_letom.append(karta)

                    if len(karte_sa_povezanim_letom) == 0:
                        raise Exception("Nemate vise karata sa mogucnosti za povezani let")
                    
                    print("{:<15} {:<20} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac"))
                    print("=" * 70)
                    for karta in karte_sa_povezanim_letom:
                        print ("{:<15} {:<20} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"]["ime"] + " " + karta["kupac"]["prezime"]))
                    print("=" * 70)

                    broj_karte = int(input("Unesite broj karte poveznog leta: >>"))
                    valja = False
                    for mogucnosti in karte_sa_povezanim_letom:
                        if mogucnosti["broj_karte"] == broj_karte:
                            valja = True
                            break
                    if not valja:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")
                    

                    korisnicka_ime_putnika = []
                    putnici = sve_karte[broj_karte]["putnici"]
                    for putnik in putnici:
                        korisnicka_ime_putnika.append(putnik["korisnicko_ime"])
                    if korisnik["korisnicko_ime"] not in korisnicka_ime_putnika:
                        raise Exception("Niste uneli validnu kartu")

                    if not korisnik["pasos"]:
                        pasos = input("Unesite broj pasosa: >>")
                    else:
                        pasos = korisnik["pasos"]
                    if not korisnik["drzavljanstvo"]:
                        drzavljanstvo = input("Unesite drzavljanstvo: >>")
                    else:
                        drzavljanstvo = korisnik["drzavljanstvo"]
                    if not korisnik["pol"]:
                        pol = input("Unesite pol: >>")
                    else:
                        pol = korisnik["pol"]

                    korisnik["pasos"] = pasos
                    korisnik["drzavljanstvo"] = drzavljanstvo
                    korisnik["pol"] = pol

                    svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                    update = kreiraj_korisnika(svi_korisnici, True, 
                                            korisnik["uloga"],
                                            korisnik["korisnicko_ime"],
                                            korisnik["korisnicko_ime"],
                                            korisnik["lozinka"],
                                            korisnik["ime"],
                                            korisnik["prezime"],
                                            korisnik["email"],
                                            korisnik["pasos"],
                                            korisnik["drzavljanstvo"],
                                            korisnik["telefon"],
                                            korisnik["pol"],
                                            )
                    sacuvaj_korisnike("korisnici.csv", "|", update)

                    if not korisnik["pasos"]:
                        raise Exception("Morate uneti broj pasosa da biste se prijavili na let")

                    if not korisnik["drzavljanstvo"]:
                        raise Exception("Morate uneti drzavljanstvo da biste se prijavili na let")

                    if not korisnik["pol"]:
                        raise Exception("Morate uneti pol da biste se prijavili na let")


                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    

                    broj_konkretnog_leta = sve_karte[broj_karte]["sifra_konkretnog_leta"]
                    broj_leta_sa_karte = svi_konkretni_letovi[broj_konkretnog_leta]["broj_leta"]
                    model = svi_letovi[broj_leta_sa_karte]["model"]

                    broj_redova = model["broj_redova"]
                    sedista = model["pozicije_sedista"]

                    matrica = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    print("=" * 50)
                    for i in range(broj_redova):
                        red = matrica[i]
                        stampa = []
                        for j in range(len(sedista)):
                            if red[j]:
                                stampa.append("X")
                            if not red[j]:
                                stampa.append(sedista[j])
                        
                        print(f"{i+1}.  {' '.join(stampa)}")
                    print("=" * 50)

                    unos_sediste = input("Unesite zeljeno sediste (A1): >>")

                    if not unos_sediste[0].isalpha() or not unos_sediste[1:].isdecimal():
                        raise Exception("Niste uneli validan format sedista")
                    if unos_sediste[0].upper() not in sedista:
                        raise Exception("Uneli ste nepostojece slovo")
                    if int(unos_sediste[1:]) > broj_redova or int(unos_sediste[1:]) <= 0:
                        raise Exception("Uneli ste los broj reda")
                    
                    odabrani_red = int(unos_sediste[1:])
                    odabrana_pozicija = unos_sediste[0].upper()
                    
                    novi_konkretni_let, nova_karta = checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[broj_konkretnog_leta], odabrani_red, odabrana_pozicija)

                    svi_konkretni_letovi_novi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    
                    svi_konkretni_letovi_novi[novi_konkretni_let["sifra"]] = novi_konkretni_let
                    sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi_novi)

                    sve_karte_nove = ucitaj_karte_iz_fajla("karte.csv", "|")

                    putnici_update = nova_karta["putnici"]
                    for putnik in range(len(putnici_update)):
                        if putnici_update[putnik]["korisnicko_ime"] == korisnik["korisnicko_ime"]:
                            putnici_update[putnik]["pasos"] = pasos
                            putnici_update[putnik]["drzavljanstvo"] = drzavljanstvo
                            putnici_update[putnik]["pol"] = pol
                    nova_karta["kupac"] = ko_je_ulogovan()   
                    nova_karta["putnici"] = putnici_update
                    sve_karte_nove[nova_karta["broj_karte"]] = nova_karta
                    sacuvaj_karte(sve_karte_nove, "karte.csv", "|")

                    
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")

                gotovo = True
                        
        elif opcija == "b":
            clear()
            return
        else:
            clear()
            print("uneli ste nepostojecu opciju")
            input("Pritisnite enter za nazad")

def prodaj_kartu():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prodaja karte")
            print("=" * 50)

            prodavac = ko_je_ulogovan()
            trazenje_letova()
            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            broj_konkretnog_leta = int(input("Unesite sifru konkretnog leta: >>"))
            if broj_konkretnog_leta not in svi_konkretni_letovi:
                raise Exception("Uneli ste nepostojeci broj konkretnog leta")

            slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

            ima_mesta = False

            for red in slobodna_mesta:      #provera da li ima mesta
                if ima_mesta:
                    break
                for sediste in red:
                    if not sediste:
                        ima_mesta = True
                        break
                
            if not ima_mesta:
                raise Exception("Na letu nema slobodnih mesta")
            

            putnici = []
            user_input = None
            while user_input != "1" and user_input != "2":
                clear()
                print("Da li kartu kupujete za registrovanog ili neregistrovanog?")
                print("1. Za registrovanog kupca")
                print("2. Za neregistrovanog kupca")
                user_input = input(">>")
                if user_input == "1":
                    svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                    registrovan = input("Unesite korisnocko ime kupca: >>")
                    if registrovan not in svi_korisnici:
                        raise Exception("Uneto korisnicko ime ne postoji")
                    kupac = svi_korisnici[registrovan]
                    if not kupac["email"]:
                        email_kupca = input("Unesite email kupca: >>")
                        kupac["email"] = email_kupca
                    if not kupac["telefon"]:
                        telefon_kupca = input("Unesite telefon kupca: >>")
                        kupac["telefon"] = telefon_kupca

                    azurirani_svi_korisnici = kreiraj_korisnika(svi_korisnici,
                                                                True,
                                                                kupac["uloga"],
                                                                kupac["korisnicko_ime"],
                                                                kupac["korisnicko_ime"],
                                                                kupac["lozinka"],
                                                                kupac["ime"],
                                                                kupac["prezime"],
                                                                kupac["email"],
                                                                kupac["pasos"],
                                                                kupac["drzavljanstvo"],
                                                                kupac["telefon"],
                                                                kupac["pol"]
                                                                )
                    sacuvaj_korisnike("korisnci.csv", "|", azurirani_svi_korisnici)
                    
                    putnici.append(kupac)
                    continue
                elif user_input == "2":
                    ime_neregistrovanog = input("Unesite ime osobe: >>")
                    prezime_neregistrovanog = input("Unesite prezime osobe: >>")
                    pasos_neregistrovanog = input("Unesite broj pasosa osobe(opciono): >>")
                    drzavljanstvo_neregistrovanog = input("Unesite drzavljanstvo osobe(opciono): >>")
                    pol_neregistrovanog = input("Unesite pol osobe(opciono): >>")
                    neregistrovani_recnik = {
                        "ime": ime_neregistrovanog,
                        "prezime": prezime_neregistrovanog,
                        "korisnicko_ime": ime_neregistrovanog+prezime_neregistrovanog
                        }

                    neregistrovani_recnik["pasos"] = pasos_neregistrovanog
                    neregistrovani_recnik["drzavljanstvo"] = drzavljanstvo_neregistrovanog
                    neregistrovani_recnik["pol"] = pol_neregistrovanog
                    neregistrovani_recnik["uloga"] = common.konstante.ULOGA_KORISNIK
                    kupac = neregistrovani_recnik
                    putnici.append(kupac)
                    continue
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")

            
            potvrda = None
            while potvrda != "da" and potvrda != "ne":
                print("Da li zelite da kupite sledecu kartu(da/ne):")
                print(f"Broj leta: {broj_konkretnog_leta}")
                print("Za putnike:")
                for putnik in putnici:
                    print(f'    {putnik["ime"]} {putnik["prezime"]}')
                potvrda = input(">>")
                if potvrda == "da":
                    continue
                elif potvrda == "ne":
                    raise Exception("Odustali ste od kupovine karte")
                else:
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


            datum_prodaje = datetime.now().replace(microsecond = 0)
            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            karta, sve_karte_nove = kupovina_karte(
                            sve_karte,
                            svi_konkretni_letovi,
                            broj_konkretnog_leta,
                            putnici,
                            slobodna_mesta,
                            kupac,
                            prodavac = prodavac,
                            datum_prodaje = datum_prodaje
                           )
            sacuvaj_karte(sve_karte_nove, "karte.csv", "|")
            
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    
    while True:
        clear()
        print("Uspesno ste kupili kartu!")
        print("=" * 50)
        print("Izaberite jednu od opcija:")
        print("1. Kupite kartu za povezani let")
        print("2. Kupite kartu za saputnika")
        print("b. Zavrsite sa kupovinom")
        opcija = input(">>")
        if opcija == "1":
            gotovo = False
            while not gotovo:
                try:
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    povezani_letovi_opcije = povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[broj_konkretnog_leta])
                    
                    print ("{:<10} {:<10} {:<20} {:<20}".format("Broj leta", "Sifra", "Polazak", "Dolazak"))
                    print("=" * 60)
                    for povezani_let in povezani_letovi_opcije:
                        datum_i_vreme_polaska = povezani_let["datum_i_vreme_polaska"].strftime("%d.%m.%y. %H:%M")
                        datum_i_vreme_dolaska = povezani_let["datum_i_vreme_dolaska"].strftime("%d.%m.%y. %H:%M")
                        print ("{:<10} {:<10} {:<20} {:<20}".format(povezani_let["broj_leta"], povezani_let["sifra"], datum_i_vreme_polaska, datum_i_vreme_dolaska))
                    print("=" * 60)

                    broj_konkretnog_leta = int(input("Unesite sifru konkretnog leta: >>"))
                    valja = False
                    for mogucnosti in povezani_letovi_opcije:
                        if mogucnosti["sifra"] == broj_konkretnog_leta:
                            valja = True
                            break
                    if not valja:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")

                    slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    ima_mesta = False

                    for red in slobodna_mesta:      #provera da li ima mesta
                        if ima_mesta:
                            break
                        for sediste in red:
                            if not sediste:
                                ima_mesta = True
                                break
                        
                    if not ima_mesta:
                        raise Exception("Na letu nema slobodnih mesta")
                    

                    putnici = []
                    
                    putnici.append(kupac)
                    

                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da kupite sledecu kartu(da/ne):")
                        print(f"Broj leta: {broj_konkretnog_leta}")
                        print("Za putnike:")
                        for putnik in putnici:
                            print(f'    {putnik["ime"]} {putnik["prezime"]}')
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            raise Exception("Odustali ste od kupovine karte")
                        else:
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")


                    datum_prodaje = datetime.now().replace(microsecond = 0)
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    karta, sve_karte_nove = kupovina_karte(
                                    sve_karte,
                                    svi_konkretni_letovi,
                                    broj_konkretnog_leta,
                                    putnici,
                                    slobodna_mesta,
                                    kupac,
                                    prodavac = prodavac,
                                    datum_prodaje = datum_prodaje
                                )
                    sacuvaj_karte(sve_karte_nove, "karte.csv", "|")
                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da kupite jos karata za povezane letove(da/ne):")
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            gotovo = True
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
        
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")


        elif opcija == "2":
            kraj = False
            while not kraj:
                try:
                    clear()
                    print("=" * 50)
                    print("Kupovina karte")
                    print("=" * 50)

                    korisnik = ko_je_ulogovan()
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    if broj_konkretnog_leta not in svi_konkretni_letovi:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")

                    slobodna_mesta = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    ima_mesta = False

                    for red in slobodna_mesta:      #provera da li ima mesta
                        if ima_mesta:
                            break
                        for sediste in red:
                            if not sediste:
                                ima_mesta = True
                                break
                        
                    if not ima_mesta:
                        raise Exception("Na letu nema slobodnih mesta")
                    

                    putnici = []
                    
                    ime_saputnika = input("Unesite ime osobe: >>")
                    prezime_saputnika = input("Unesite prezime osobe: >>")
                    pasos_saputnika = input("Unesite broj pasosa osobe(opciono): >>")
                    drzavljanstvo_saputnika = input("Unesite drzavljanstvo osobe(opciono): >>")
                    pol_saputnika = input("Unesite pol osobe(opciono): >>")
                    drugi_recnik = {
                        "ime": ime_saputnika,
                        "prezime": prezime_saputnika,
                        "korisnicko_ime": ime_saputnika+prezime_saputnika
                        }

                    drugi_recnik["pasos"] = pasos_saputnika
                    drugi_recnik["drzavljanstvo"] = drzavljanstvo_saputnika
                    drugi_recnik["pol"] = pol_saputnika
                    putnici.append(drugi_recnik)
                    
                    
                    potvrda = None
                    while potvrda != "da" and potvrda != "ne":
                        print("Da li zelite da dodate saputnika(da/ne):")
                        print(f"Broj leta: {broj_konkretnog_leta}")
                        print("Za putnike:")
                        for putnik in putnici:
                            print(f'    {putnik["ime"]} {putnik["prezime"]}')
                        potvrda = input(">>")
                        if potvrda == "da":
                            continue
                        elif potvrda == "ne":
                            raise Exception("Odustali ste od kupovine karte")
                        else:
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")



                    sve_karte_update_putnika = ucitaj_karte_iz_fajla("karte.csv", "|")
                    sve_karte_update_putnika[karta["broj_karte"]]["putnici"].extend(putnici)
                    sacuvaj_karte(sve_karte_update_putnika, "karte.csv", "|")
                    
                    jos = None
                    while jos != "da" and jos != "ne":
                        print("Da li zelite da kupite jos karata za saputnike(da/ne):")
                        jos = input(">>")
                        if jos == "da":
                            continue
                        elif jos == "ne":
                            kraj = True
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
                    
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")
            
        elif opcija == "b":
            clear()
            return
        else:
            clear()
            print("uneli ste nepostojecu opciju")
            input("Pritisnite enter za nazad")

#TODO
def prijava_na_let_prodavac():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Prijava na let")
            print("=" * 50)

            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
            prikaz_pretraga_prodatih_karata()
            

            broj_karte = int(input("Unesite broj karte: >>"))
            if broj_karte not in sve_karte:
                raise Exception("Uneli ste nepostojeci broj karte")

            korisnicka_ime_putnika = []
            putnici = sve_karte[broj_karte]["putnici"]
            for putnik in putnici:
                korisnicka_ime_putnika.append(putnik["korisnicko_ime"])
            
            kupac = sve_karte[broj_karte]["kupac"]
            if kupac["korisnicko_ime"] in svi_korisnici:  #kupac je registrovani korisnik
                if kupac["korisnicko_ime"] in korisnicka_ime_putnika:
                    putnik_za_prijavu = kupac
                elif kupac["korisnicko_ime"] not in korisnicka_ime_putnika:
                    putnik_za_prijavu = sve_karte[broj_karte]["putnici"][0]
                else:
                    raise Exception("Kupac je registrovan ali nije putnik a putnici su i/ili prazni")
            elif kupac["korisnicko_ime"] not in svi_korisnici:   #kupac je neregistrovan
                for putnik in putnici:
                    if kupac["korisnicko_ime"] == putnik["korisnicko_ime"]:
                        putnik_za_prijavu = kupac

            
            if not putnik_za_prijavu["pasos"]:
                pasos = input("Unesite broj pasosa: >>")
            else:
                pasos = putnik_za_prijavu["pasos"]
            if not putnik_za_prijavu["drzavljanstvo"]:
                drzavljanstvo = input("Unesite drzavljanstvo: >>")
            else:
                drzavljanstvo = putnik_za_prijavu["drzavljanstvo"]
            if not putnik_za_prijavu["pol"]:
                pol = input("Unesite pol: >>")
            else:
                pol = putnik_za_prijavu["pol"]

            putnik_za_prijavu["pasos"] = pasos
            putnik_za_prijavu["drzavljanstvo"] = drzavljanstvo
            putnik_za_prijavu["pol"] = pol

            if putnik_za_prijavu["korisnicko_ime"] in svi_korisnici and putnik_za_prijavu["korisnicko_ime"] in korisnicka_ime_putnika:
                svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                update = kreiraj_korisnika(svi_korisnici, True, 
                                        putnik_za_prijavu["uloga"],
                                        putnik_za_prijavu["korisnicko_ime"],
                                        putnik_za_prijavu["korisnicko_ime"],
                                        putnik_za_prijavu["lozinka"],
                                        putnik_za_prijavu["ime"],
                                        putnik_za_prijavu["prezime"],
                                        putnik_za_prijavu["email"],
                                        putnik_za_prijavu["pasos"],
                                        putnik_za_prijavu["drzavljanstvo"],
                                        putnik_za_prijavu["telefon"],
                                        putnik_za_prijavu["pol"],
                                        )
                sacuvaj_korisnike("korisnici.csv", "|", update)

            if not putnik_za_prijavu["pasos"]:
                raise Exception("Morate uneti broj pasosa da biste se prijavili na let")

            if not putnik_za_prijavu["drzavljanstvo"]:
                raise Exception("Morate uneti drzavljanstvo da biste se prijavili na let")

            if not putnik_za_prijavu["pol"]:
                raise Exception("Morate uneti pol da biste se prijavili na let")

            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            

            broj_konkretnog_leta = sve_karte[broj_karte]["sifra_konkretnog_leta"]
            broj_leta_sa_karte = svi_konkretni_letovi[broj_konkretnog_leta]["broj_leta"]
            model = svi_letovi[broj_leta_sa_karte]["model"]

            broj_redova = model["broj_redova"]
            sedista = model["pozicije_sedista"]

            matrica = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

            print("=" * 50)
            for i in range(broj_redova):
                red = matrica[i]
                stampa = []
                for j in range(len(sedista)):
                    if red[j]:
                        stampa.append("X")
                    if not red[j]:
                        stampa.append(sedista[j])
                
                print(f"{i+1}.  {' '.join(stampa)}")
            print("=" * 50)

            unos_sediste = input("Unesite zeljeno sediste (A1): >>")

            if not unos_sediste[0].isalpha() or not unos_sediste[1:].isdecimal():
                raise Exception("Niste uneli validan format sedista")
            if unos_sediste[0].upper() not in sedista:
                raise Exception("Uneli ste nepostojece slovo")
            if int(unos_sediste[1:]) > broj_redova or int(unos_sediste[1:]) <= 0:
                raise Exception("Uneli ste los broj reda")
            
            odabrani_red = int(unos_sediste[1:])
            odabrana_pozicija = unos_sediste[0].upper()
            
            novi_konkretni_let, nova_karta = checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[broj_konkretnog_leta], odabrani_red, odabrana_pozicija)

            svi_konkretni_letovi_novi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            
            svi_konkretni_letovi_novi[novi_konkretni_let["sifra"]] = novi_konkretni_let
            sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi_novi)

            sve_karte_nove = ucitaj_karte_iz_fajla("karte.csv", "|")
            putnici_update = nova_karta["putnici"]
            for putnik in range(len(putnici_update)):
                if putnici_update[putnik]["korisnicko_ime"] == putnik_za_prijavu["korisnicko_ime"]:
                    putnici_update[putnik]["pasos"] = pasos
                    putnici_update[putnik]["drzavljanstvo"] = drzavljanstvo
                    putnici_update[putnik]["pol"] = pol


            if putnik_za_prijavu["korisnicko_ime"] == kupac["korisnicko_ime"]:
                nova_karta["kupac"] = putnik_za_prijavu  
                   
            nova_karta["putnici"] = putnici_update

            sve_karte_nove[nova_karta["broj_karte"]] = nova_karta
            sacuvaj_karte(sve_karte_nove, "karte.csv", "|")

            
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    while True:
        clear()
        print("Uspesno ste se prijavili na let!")
        print("=" * 50)
        print("Izaberite jednu od opcija:")
        print("1. Prijavite se na povezani let")
        print("b. Zavrsite sa prijavnom na letove")
        opcija = input(">>")
        if opcija == "1":
            gotovo = False
            while not gotovo:
                try:
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    povezani_letovi_opcije = povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[broj_konkretnog_leta])

                    korisnikove_karte = pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi, "","","" ,"" , putnik_za_prijavu["korisnicko_ime"])
                    karte_sa_povezanim_letom = []

                    for karta in korisnikove_karte:
                        for povezani_let in povezani_letovi_opcije:
                            if karta["sifra_konkretnog_leta"] == povezani_let["sifra"]:
                                karte_sa_povezanim_letom.append(karta)

                    if len(karte_sa_povezanim_letom) == 0:
                        raise Exception("Nemate vise karata sa mogucnosti za povezani let")
                    
                    print("{:<15} {:<20} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac"))
                    print("=" * 70)
                    for karta in karte_sa_povezanim_letom:
                        print ("{:<15} {:<20} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"]["ime"] + " " + karta["kupac"]["prezime"]))
                    print("=" * 70)

                    broj_karte = int(input("Unesite broj karte poveznog leta: >>"))
                    valja = False
                    for mogucnosti in karte_sa_povezanim_letom:
                        if mogucnosti["broj_karte"] == broj_karte:
                            valja = True
                            break
                    if not valja:
                        raise Exception("Uneli ste nepostojeci broj konkretnog leta")
                    
                    korisnicka_ime_putnika = []
                    putnici = sve_karte[broj_karte]["putnici"]
                    for putnik in putnici:
                        korisnicka_ime_putnika.append(putnik["korisnicko_ime"])
                    
                    kupac = sve_karte[broj_karte]["kupac"]
                    if kupac["korisnicko_ime"] in svi_korisnici:  #kupac je registrovani korisnik
                        if kupac["korisnicko_ime"] in korisnicka_ime_putnika:
                            putnik_za_prijavu = kupac
                        elif kupac["korisnicko_ime"] not in korisnicka_ime_putnika:
                            putnik_za_prijavu = sve_karte[broj_karte]["putnici"][0]
                        else:
                            raise Exception("Kupac je registrovan ali nije putnik a putnici su i/ili prazni")
                    elif kupac["korisnicko_ime"] not in svi_korisnici:   #kupac je neregistrovan
                        for putnik in putnici:
                            if kupac["korisnicko_ime"] == putnik["korisnicko_ime"]:
                                putnik_za_prijavu = kupac
                    
                    if not putnik_za_prijavu["pasos"]:
                        pasos = input("Unesite broj pasosa: >>")
                    else:
                        pasos = putnik_za_prijavu["pasos"]
                    if not putnik_za_prijavu["drzavljanstvo"]:
                        drzavljanstvo = input("Unesite drzavljanstvo: >>")
                    else:
                        drzavljanstvo = putnik_za_prijavu["drzavljanstvo"]
                    if not putnik_za_prijavu["pol"]:
                        pol = input("Unesite pol: >>")
                    else:
                        pol = putnik_za_prijavu["pol"]

                    putnik_za_prijavu["pasos"] = pasos
                    putnik_za_prijavu["drzavljanstvo"] = drzavljanstvo
                    putnik_za_prijavu["pol"] = pol

                    if putnik_za_prijavu["korisnicko_ime"] in svi_korisnici and putnik_za_prijavu["korisnicko_ime"] in korisnicka_ime_putnika:
                        svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                        update = kreiraj_korisnika(svi_korisnici, True, 
                                                putnik_za_prijavu["uloga"],
                                                putnik_za_prijavu["korisnicko_ime"],
                                                putnik_za_prijavu["korisnicko_ime"],
                                                putnik_za_prijavu["lozinka"],
                                                putnik_za_prijavu["ime"],
                                                putnik_za_prijavu["prezime"],
                                                putnik_za_prijavu["email"],
                                                putnik_za_prijavu["pasos"],
                                                putnik_za_prijavu["drzavljanstvo"],
                                                putnik_za_prijavu["telefon"],
                                                putnik_za_prijavu["pol"],
                                                )
                        sacuvaj_korisnike("korisnici.csv", "|", update)

                    if not putnik_za_prijavu["pasos"]:
                        raise Exception("Morate uneti broj pasosa da biste se prijavili na let")

                    if not putnik_za_prijavu["drzavljanstvo"]:
                        raise Exception("Morate uneti drzavljanstvo da biste se prijavili na let")

                    if not putnik_za_prijavu["pol"]:
                        raise Exception("Morate uneti pol da biste se prijavili na let")
                

                    svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                    

                    broj_konkretnog_leta = sve_karte[broj_karte]["sifra_konkretnog_leta"]
                    broj_leta_sa_karte = svi_konkretni_letovi[broj_konkretnog_leta]["broj_leta"]
                    model = svi_letovi[broj_leta_sa_karte]["model"]

                    broj_redova = model["broj_redova"]
                    sedista = model["pozicije_sedista"]

                    matrica = svi_konkretni_letovi[broj_konkretnog_leta]["zauzetost"]

                    print("=" * 50)
                    for i in range(broj_redova):
                        red = matrica[i]
                        stampa = []
                        for j in range(len(sedista)):
                            if red[j]:
                                stampa.append("X")
                            if not red[j]:
                                stampa.append(sedista[j])
                        
                        print(f"{i+1}.  {' '.join(stampa)}")
                    print("=" * 50)

                    unos_sediste = input("Unesite zeljeno sediste (A1): >>")

                    if not unos_sediste[0].isalpha() or not unos_sediste[1:].isdecimal():
                        raise Exception("Niste uneli validan format sedista")
                    if unos_sediste[0].upper() not in sedista:
                        raise Exception("Uneli ste nepostojece slovo")
                    if int(unos_sediste[1:]) > broj_redova or int(unos_sediste[1:]) <= 0:
                        raise Exception("Uneli ste los broj reda")
                    
                    odabrani_red = int(unos_sediste[1:])
                    odabrana_pozicija = unos_sediste[0].upper()
                    
                    novi_konkretni_let, nova_karta = checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[broj_konkretnog_leta], odabrani_red, odabrana_pozicija)

                    svi_konkretni_letovi_novi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                    
                    svi_konkretni_letovi_novi[novi_konkretni_let["sifra"]] = novi_konkretni_let
                    sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi_novi)

                    sve_karte_nove = ucitaj_karte_iz_fajla("karte.csv", "|")
                    putnici_update = nova_karta["putnici"]
                    for putnik in range(len(putnici_update)):
                        if putnici_update[putnik]["korisnicko_ime"] == putnik_za_prijavu["korisnicko_ime"]:
                            putnici_update[putnik]["pasos"] = pasos
                            putnici_update[putnik]["drzavljanstvo"] = drzavljanstvo
                            putnici_update[putnik]["pol"] = pol


                    if putnik_za_prijavu["korisnicko_ime"] == kupac["korisnicko_ime"]:
                        nova_karta["kupac"] = putnik_za_prijavu  
                        
                    nova_karta["putnici"] = putnici_update

                    sve_karte_nove[nova_karta["broj_karte"]] = nova_karta
                    sacuvaj_karte(sve_karte_nove, "karte.csv", "|")
                except Exception as message:
                    user_input = None
                    while user_input != "1" and user_input != "b":
                        clear()
                        print("Los unos!")
                        print(message)
                        print("1. Pokusajte ponovo")
                        print("b. nazad")
                        user_input = input(">>")
                        if user_input == "1":
                            continue
                        elif user_input == "b":
                            clear()
                            return
                        else:
                            clear()
                            print("uneli ste nepostojecu opciju")
                            input("Pritisnite enter za nazad")

                gotovo = True
                        
        elif opcija == "b":
            clear()
            return
        else:
            clear()
            print("uneli ste nepostojecu opciju")
            input("Pritisnite enter za nazad")
    
def izmeni_kartu():
    prikaz_pretraga_prodatih_karata()
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Izmena karte")
            print("=" * 50)

            broj_karte = int(input("Unesite broj karte za izmenu: >>"))

            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            
            if broj_karte not in sve_karte:
                raise Exception("Broj karte ne psotoji")
            karta_za_izmenu = sve_karte[broj_karte]


            sifra_konkretnog_leta = input("Unesite broj konkretnog leta: >>")
            if sifra_konkretnog_leta:
                karta_za_izmenu["sifra_konkretnog_leta"] = sifra_konkretnog_leta

            sediste = input("Unesite sediste: >>")
            if sediste:
                karta_za_izmenu["sediste"] = sediste

            datum_prodaje = input("Unesite datum prodaje karte(dd.mm.yyyy. HH:MM): >>")
            if datum_prodaje:
                try:
                    datum_prodaje = datetime.strptime(datum_prodaje, "%d.%m.%Y. %H:%M")
                    karta_za_izmenu["datum_prodaje"] = datum_prodaje
                except:
                    raise Exception("datum prodaje karte nije odgovarajuceg formata")


            nova_karta = izmena_karte(sve_karte,
                                    svi_konkretni_letovi,
                                    broj_karte,
                                    karta_za_izmenu["sifra_konkretnog_leta"],
                                    karta_za_izmenu["datum_prodaje"],
                                    karta_za_izmenu["sediste"]
                                    )
            sacuvaj_karte(nova_karta,"karte.csv", "|")
            uspesno = True

        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    input("Uspesno ste izmenili kartu!\nPritisnite enter za nazad")

def oznaci_za_brisanje_karata():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Oznacavanje karata za brisanje")
            print("=" * 50)

            prikaz_pretraga_prodatih_karata()

            broj_karte = input("Unesite broj karte: >>")

            if not broj_karte.isdecimal():
                raise Exception("Broj karte mora biti broj")

            broj_karte = int(broj_karte)

            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            
            karte = brisanje_karte(ko_je_ulogovan(), sve_karte, broj_karte)

            sacuvaj_karte(karte, "karte.csv", "|")      

            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")

    print("=" * 70)
    print("SLEDECA KARTA JE OZNACENA ZA BRISANJE")
    #print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
    print("{:<15} {:<20} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac"))
    print("=" * 70)
    karta = sve_karte[broj_karte]
    print ("{:<15} {:<20} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"]["ime"] + " " + karta["kupac"]["prezime"]))
    # datum_prodaje = karta["datum_prodaje"].strftime("%d.%m.%y.")
    # print ("{:<15} {:<20} {:<15} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"], datum_prodaje))
    print("=" * 70)
    input("Pritisnite bilo koji taster za nazad")

def prikaz_pretraga_prodatih_karata(korisnik = None):
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Pretraga prodatih karata")
            print("=" * 50)
            polaziste = input("Unesite polaziste: >>")
            odrediste = input("Unesite odrediste: >>")
            datum_polaska = input("Unesite datum polaska(dd.mm.yyyy.): >>")
            if  not datum_polaska:
                pass
            else:
                datum_polaska = datetime.strptime(datum_polaska, "%d.%m.%Y.")
            
            datum_dolaska = input("Unesite datum dolaska(dd.mm.yyyy.): >>")
            if not datum_dolaska:
                pass
            else:
                datum_dolaska = datetime.strptime(datum_dolaska, "%d.%m.%Y.")
            
            if not korisnik:
                korisnico_ime_putnika = input("Unesite korisnicko ime putnika: >>")
            else:
                korisnico_ime_putnika = korisnik
            
            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            
            karte = pretraga_prodatih_karata(sve_karte, svi_letovi, konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, korisnico_ime_putnika)
            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")


    #print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
    print("{:<15} {:<20} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac"))

    print("=" * 70)
    for karta in karte:
        #datum_prodaje = karta["datum_prodaje"].strftime("%d.%m.%y.")
        #print ("{:<15} {:<20} {:<15} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"], datum_prodaje))
        print ("{:<15} {:<20} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"]["ime"] + " " + karta["kupac"]["prezime"]))
    print("=" * 70)
    input("Pritisnite bilo koji taster za nazad")

def registrovanje_novih_prodavaca():
    
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Registracija novih prodavaca")
            print("=" * 50)
            korisnicko_ime = input("Unesite korisnicko ime: >>")
            lozinka = input("Unesite lozinku: >>")
            ime = input("Unesite ime: >>")
            prezime = input("Unesite prezime: >>")
            

            svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")

            kreiraj_korisnika(svi_korisnici, False, common.konstante.ULOGA_PRODAVAC, "", korisnicko_ime, lozinka, ime, prezime)
            sacuvaj_korisnike("korisnici.csv", "|", svi_korisnici)

            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    input("Uspesno ste se registrovali!\nPritisnite enter za nazad")

def kreiraj_let():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Kreiranje leta")
            print("=" * 50)
            broj_leta = input("Unesite broj leta: >>")
            sifra_polazisnog_aerodroma = input("Unesite sifru polazisnog aerodroma: >>")
            sifra_odredisnog_aerodroma = input("Unesite sifru odredisnog aerodroma: >>")
            vreme_poletanja = input("Unesite vreme poletanja (HH:MM): >>")
            vreme_sletanja = input("Unesite vreme sletanja (HH:MM): >>")

            sletanje_sutra = input("Sletanje sutra (da/ne): >>")

            if sletanje_sutra.lower() == "da":
                sletanje_sutra = True
            elif sletanje_sutra.lower() == "ne":
                sletanje_sutra = False
            else:
                raise Exception("Niste uneli validnu vrednost za sletanje sutra")

            prevoznik = input("Unesite prevoznika: >>")

            dani = input("Unesite dane odvojene zarezima (1,2,3,4,5,6,7): >>")
            dani.replace(" ", "")
            dani = dani.split(",")
            for i in range(len(dani)):
                if not dani[i].isdecimal():
                    raise Exception("Dan mora biti broj od 1-7")
                dani[i] = int(dani[i])-1
                if dani[i] not in (common.konstante.PONEDELJAK, common.konstante.UTORAK, common.konstante.SREDA, common.konstante.CETVRTAK, common.konstante.PETAK, common.konstante.SUBOTA, common.konstante.NEDELJA):
                    raise Exception("Nisu uneti validni dani")
            
            id_modela_aviona = input("Unesite id modela aviona: >>")
            modeli = ucitaj_modele_aviona("modeli_aviona.csv", "|")

            if not id_modela_aviona.isdecimal():
                raise Exception("id modela aviona mora biti broj")
            id_modela_aviona = int(id_modela_aviona)
            if id_modela_aviona not in modeli:
                raise Exception("Uneti model aviona ne postoji")

            model_aviona = modeli[id_modela_aviona]


            cena = input("Unesite cenu (. ako ima decimala): >>")
            if cena.isdecimal() or ("." in cena and cena.replace(".", "").isdecimal()):
                cena = float(cena)
            else:
                raise Exception("Cena nije validnog formata")
            
            datum_pocetka_operativnosti = input("Unesite datum pocetka operativnosti(dd.mm.yyyy. HH:MM): >>")
            try:
                datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, "%d.%m.%Y. %H:%M")
            except:
                raise Exception("datum pocetka operativnosti nije odgovarajuceg formata")
            
            datum_kraja_operativnosti = input("Unesite datum kraja operativnosti(dd.mm.yyyy. HH:MM): >>")
            try:
                datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, "%d.%m.%Y. %H:%M")
            except:
                raise Exception("datum kraja operativnosti nije odgovarajuceg formata")

            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")

            novi_let = kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model_aviona, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
            sacuvaj_letove("letovi.csv", "|", novi_let)

            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            novi_konkretni_letovi = kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
            for konkretan_let in novi_konkretni_letovi:
                if novi_konkretni_letovi[konkretan_let]["broj_leta"] == broj_leta:
                    novi_konkretni_letovi[konkretan_let]["zauzetost"] = podesi_matricu_zauzetosti(svi_letovi, novi_konkretni_letovi[konkretan_let])
            sacuvaj_kokretan_let("konkretni_letovi.csv", "|", novi_konkretni_letovi)

            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    input("Uspesno ste kreirali let!\nPritisnite enter za nazad")

def izmeni_let():
    trazenje_letova()
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Izmena leta")
            print("=" * 50)

            broj_leta = input("Unesite broj leta za izmenu: >>")

            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            
            if broj_leta not in svi_letovi:
                raise Exception("Broj leta ne psotoji")
            let_za_izmenu = svi_letovi[broj_leta]


            sifra_polazisnog_aerodroma = input("Unesite sifru polazisnog aerodroma: >>")
            if sifra_polazisnog_aerodroma:
                let_za_izmenu["sifra_polazisnog_aerodroma"] = sifra_polazisnog_aerodroma

            sifra_odredisnog_aerodroma = input("Unesite sifru odredisnog aerodroma: >>")
            if sifra_odredisnog_aerodroma:
                let_za_izmenu["sifra_odredisnog_aerodorma"] = sifra_odredisnog_aerodroma

            vreme_poletanja = input("Unesite vreme poletanja (HH:MM): >>")
            if vreme_poletanja:
                let_za_izmenu["vreme_poletanja"] = vreme_poletanja

            vreme_sletanja = input("Unesite vreme sletanja (HH:MM): >>")
            if vreme_sletanja:
                let_za_izmenu["vreme_sletanja"] = vreme_sletanja

            sletanje_sutra = input("Sletanje sutra (da/ne): >>")
            if sletanje_sutra:
                if sletanje_sutra.lower() == "da":
                    sletanje_sutra = True
                    let_za_izmenu["sletanje_sutra"] = sletanje_sutra
                elif sletanje_sutra.lower() == "ne":
                    sletanje_sutra = False
                    let_za_izmenu["sletanje_sutra"] = sletanje_sutra
                else:
                    raise Exception("Niste uneli validnu vrednost za sletanje sutra")

            prevoznik = input("Unesite prevoznika: >>")
            if prevoznik:
                let_za_izmenu["prevoznik"] = prevoznik

            dani = input("Unesite dane odvojene zarezima (1,2,3,4,5,6,7): >>")
            if dani:
                dani.replace(" ", "")
                dani = dani.split(",")
                for i in range(len(dani)):
                    if not dani[i].isdecimal():
                        raise Exception("Dan mora biti broj od 1-7")
                    dani[i] = int(dani[i])-1
                    if dani[i] not in (common.konstante.PONEDELJAK, common.konstante.UTORAK, common.konstante.SREDA, common.konstante.CETVRTAK, common.konstante.PETAK, common.konstante.SUBOTA, common.konstante.NEDELJA):
                        raise Exception("Nisu uneti validni dani")
                
                let_za_izmenu["dani"] = dani

            id_modela_aviona = input("Unesite id modela aviona: >>")
            if id_modela_aviona:
                
                modeli = ucitaj_modele_aviona("modeli_aviona.csv", "|")

                if not id_modela_aviona.isdecimal():
                    raise Exception("id modela aviona mora biti broj")
                id_modela_aviona = int(id_modela_aviona)
                if id_modela_aviona not in modeli:
                    raise Exception("Uneti model aviona ne postoji")

                model_aviona = modeli[id_modela_aviona]
                let_za_izmenu["model"] = model_aviona

            cena = input("Unesite cenu (. ako ima decimala): >>")
            if cena:
                if cena.isdecimal() or ("." in cena and cena.replace(".", "").isdecimal()):
                    cena = float(cena)
                    let_za_izmenu["cena"] = cena
                else:
                    raise Exception("Cena nije validnog formata")
            
            datum_pocetka_operativnosti = input("Unesite datum pocetka operativnosti(dd.mm.yyyy. HH:MM): >>")
            if datum_pocetka_operativnosti:
                try:
                    datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, "%d.%m.%Y. %H:%M")
                    let_za_izmenu["datum_pocetka_operativnosti"] = datum_pocetka_operativnosti
                except:
                    raise Exception("datum pocetka operativnosti nije odgovarajuceg formata")
            
            datum_kraja_operativnosti = input("Unesite datum kraja operativnosti(dd.mm.yyyy. HH:MM): >>")
            if datum_kraja_operativnosti:
                try:
                    datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, "%d.%m.%Y. %H:%M")
                    let_za_izmenu["datum_kraja_operativnosti"] = datum_kraja_operativnosti
                except:
                    raise Exception("datum kraja operativnosti nije odgovarajuceg formata")



            novi_let = izmena_letova(svi_letovi,
                                    broj_leta,
                                    let_za_izmenu["sifra_polazisnog_aerodroma"],
                                    let_za_izmenu["sifra_odredisnog_aerodorma"],
                                    let_za_izmenu["vreme_poletanja"],
                                    let_za_izmenu["vreme_sletanja"],
                                    let_za_izmenu["sletanje_sutra"],
                                    let_za_izmenu["prevoznik"],
                                    let_za_izmenu["dani"],
                                    let_za_izmenu["model"],
                                    let_za_izmenu["cena"],
                                    let_za_izmenu["datum_pocetka_operativnosti"],
                                    let_za_izmenu["datum_kraja_operativnosti"])
            sacuvaj_letove("letovi.csv", "|", novi_let)

            svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
            svi_konkretni_letovi_copy = {}
            
            for konkretan_let in svi_konkretni_letovi:
                if svi_konkretni_letovi[konkretan_let]["broj_leta"] != broj_leta:
                    # del svi_konkretni_letovi_copy[konkretan_let]
                    svi_konkretni_letovi_copy[konkretan_let] = svi_konkretni_letovi[konkretan_let]
                

            novi_konkretni_letovi = kreiranje_konkretnog_leta(svi_konkretni_letovi_copy, svi_letovi[broj_leta])
            for konkretan_let in novi_konkretni_letovi:
                if novi_konkretni_letovi[konkretan_let]["broj_leta"] == broj_leta:
                    novi_konkretni_letovi[konkretan_let]["zauzetost"] = podesi_matricu_zauzetosti(svi_letovi, novi_konkretni_letovi[konkretan_let])
            sacuvaj_kokretan_let("konkretni_letovi.csv", "|", novi_konkretni_letovi)


            uspesno = True
        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Los unos!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    clear()
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")
    clear()
    input("Uspesno ste izmenili let!\nPritisnite enter za nazad")

def zapravo_obrisi_kartu():
    uspesno = False
    while not uspesno:
        try:
            clear()
            print("=" * 50)
            print("Trajno brisanje karata")
            print("=" * 50) 
            print("{:<5} {:<15} {:<25}".format("Index", "Broj karte", "Kupac"))

            sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
            oznaceni = []

            index = 0
            for broj_karte in sve_karte:
                if sve_karte[broj_karte]["obrisana"]:
                    index += 1
                    print("{:<5} {:<15} {:<25}".format(index, broj_karte, sve_karte[broj_karte]["kupac"]["korisnicko_ime"]))
                    oznaceni.append((index, broj_karte))
            print("=" * 50)
            print("Za brisanje svih karata uneti os")
            print("Za brisanje jedne karte uneti o pa njen index")
            print("Za brisanje vise karata uneti o pa njihove indexe odvojene zarezima")
            print("Za vracanje svih karata uneti vs")
            print("Za vracanje jedne karte uneti v pa njen index")
            print("Za vracanje vise karata uneti v pa njihove indexe odvojene zarezima")
            print("=" * 50)
            index_unos = input("Unesite uputstvo za brisanje: >>")
            if index_unos[0].lower() != "o" and  index_unos[0].lower() != "v":
                raise Exception("Niste uneli validnu naredbu")
            elif index_unos == "os":
                for tuple in oznaceni:
                    index_za_brisanje_sve = tuple[1]
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    karte = brisanje_karte(ko_je_ulogovan(), sve_karte, index_za_brisanje_sve)
                    sacuvaj_karte(karte, "karte.csv", "|")
            elif index_unos == "vs":
                for tuple in oznaceni:
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    sve_karte[tuple[1]]["obrisana"] = False
                    sacuvaj_karte(sve_karte, "karte.csv", "|")
            elif "," not in index_unos and index_unos[0] == "o":
                index_unos = index_unos[1:]
                if not index_unos.isdecimal():
                    raise Exception("Broj karte mora biti broj")
                else:
                    index_unos = int(index_unos)
                    for tuple in oznaceni:
                        if tuple[0] == index_unos:
                            index_za_brisanje_jedne = tuple[1]
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    karte = brisanje_karte(ko_je_ulogovan(), sve_karte, index_za_brisanje_jedne)
                    sacuvaj_karte(karte, "karte.csv", "|")      
            elif "," in index_unos and index_unos[0] == "o":
                index_unos = index_unos[1:]
                broj_karte_lista = index_unos.split(",")
                for i in broj_karte_lista:
                    if not i.isdecimal():
                        raise Exception("Broj karte mora biti broj")
                    index_unos = int(i)
                    for tuple in oznaceni:
                        if tuple[0] == index_unos:
                            index_za_brisanje_vise = tuple[1]
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    karte = brisanje_karte(ko_je_ulogovan(), sve_karte, index_za_brisanje_vise)
                    sacuvaj_karte(karte, "karte.csv", "|")  
            elif "," not in index_unos and index_unos[0] == "v":
                index_unos = index_unos[1:]
                if not index_unos.isdecimal():
                    raise Exception("Broj karte mora biti broj")
                else:
                    index_unos = int(index_unos)
                    for tuple in oznaceni:
                        if tuple[0] == index_unos:
                            broj_karte_za_vracanje_jedne = tuple[1]
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    sve_karte[broj_karte_za_vracanje_jedne]["obrisana"] = False
                    sacuvaj_karte(sve_karte, "karte.csv", "|")      
            elif "," in index_unos and index_unos[0] == "v":
                index_unos = index_unos[1:]
                broj_karte_lista = index_unos.split(",")
                for i in broj_karte_lista:
                    if not i.isdecimal():
                        raise Exception("Broj karte mora biti broj")
                    index_unos = int(i)
                    for tuple in oznaceni:
                        if tuple[0] == index_unos:
                            broj_karte_za_vracanje_vise = tuple[1]
                    sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                    sve_karte[broj_karte_za_vracanje_vise]["obrisana"] = False
                    sacuvaj_karte(sve_karte, "karte.csv", "|")  
            else:
                raise Exception("Nesto je poslo po zlu")
            uspesno = True

        except Exception as message:
            user_input = None
            while user_input != "1" and user_input != "b":
                clear()
                print("Pogresni parametri!")
                print(message)
                print("1. Pokusajte ponovo")
                print("b. nazad")
                user_input = input(">>")
                if user_input == "1":
                    continue
                elif user_input == "b":
                    return
                else:
                    clear()
                    print("uneli ste nepostojecu opciju")
                    input("Pritisnite enter za nazad")

    print("=" * 40)
    print("NAREDBA USPESNO IZVRSENA")
    # print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
    print("=" * 40)
    # karta = sve_karte[broj_karte]
    # datum_prodaje = karta["datum_prodaje"].strftime("%d.%m.%y.")
    # print ("{:<15} {:<20} {:<15} {:<15}".format(karta["broj_karte"], karta["sifra_konkretnog_leta"], karta["kupac"], datum_prodaje))
    # print("=" * 70)
    input("Pritisnite bilo koji taster za nazad")

def generisi_izvestaje():

    def prikazi_izvestaj_prodatih_karata_za_dan_prodaje():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan prodaje")
                print("=" * 50)
                
                dan = input("Unesite datum prodaje(dd.mm.yyyy.): >>")

                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan prodaje nije odgovarajuceg formata")

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                
                izvestaj = izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, dan)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
        print("=" * 70)
        for rezultat in izvestaj:
            datum_prodaje = rezultat["datum_prodaje"].strftime("%d.%m.%y.")
            print ("{:<15} {:<20} {:<15} {:<15}".format(rezultat["broj_karte"], rezultat["sifra_konkretnog_leta"], rezultat["kupac"]["korisnicko_ime"], datum_prodaje))
        print("=" * 70)
        input("Pritisnite bilo koji taster za nazad")


    def prikazi_izvestaj_prodatih_karata_za_dan_polaska():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan polaska")
                print("=" * 50)
                
                dan = input("Unesite datum polaska(dd.mm.yyyy.): >>")
                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan polaska nije odgovarajuceg formata")


                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                
                izvestaj = izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, dan)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
        print("=" * 70)
        for rezultat in izvestaj:
            if rezultat["datum_prodaje"] != "":
                datum_prodaje = rezultat["datum_prodaje"].strftime("%d.%m.%y.")
            else:
                datum_prodaje = ""
            print ("{:<15} {:<20} {:<15} {:<15}".format(rezultat["broj_karte"], rezultat["sifra_konkretnog_leta"], rezultat["kupac"]["korisnicko_ime"], datum_prodaje))
        print("=" * 70)
        input("Pritisnite bilo koji taster za nazad")

    def prikazi_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan prodaje i prodavca")
                print("=" * 50)
                
                dan = input("Unesite datum prodaje(dd.mm.yyyy.): >>")
                
                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan prodaje nije odgovarajuceg formata")
                
                korsnicko_ime_prodavac = input("Unesite prodavca: >>")
                svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                prodavac = svi_korisnici[korsnicko_ime_prodavac]

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                
                izvestaj = izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan, prodavac)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<15} {:<20} {:<15} {:<15}".format("Broj karte", "Sifra konkretnog leta", "Kupac", "Datum prodaje"))
        print("=" * 70)
        for rezultat in izvestaj:
            datum_prodaje = rezultat["datum_prodaje"].strftime("%d.%m.%y.")
            print ("{:<15} {:<20} {:<15} {:<15}".format(rezultat["broj_karte"], rezultat["sifra_konkretnog_leta"], rezultat["kupac"]["korisnicko_ime"], datum_prodaje))
        print("=" * 70)
        input("Pritisnite bilo koji taster za nazad")


    def prikazi_izvestaj_ubc_prodatih_karata_za_dan_prodaje():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan prodaje")
                print("=" * 50)
                
                dan = input("Unesite datum prodaje(dd.mm.yyyy.): >>")

                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan prodaje nije odgovarajuceg formata")

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                izvestaj = izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi, dan)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<30} {:<30}".format("Ukupan broj karata", "Ukupna cena karata"))
        print("=" * 60)
        print ("{:<30} {:<30}".format(izvestaj[0], izvestaj[1]))
        print("=" * 60)
        input("Pritisnite bilo koji taster za nazad")

    def prikazi_izvestaj_ubc_prodatih_karata_za_dan_polaska():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan polaska")
                print("=" * 50)
                
                dan = input("Unesite datum polaska(dd.mm.yyyy.): >>")
                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan polaska nije odgovarajuceg formata")

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                izvestaj = izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi, dan)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<30} {:<30}".format("Ukupan broj karata", "Ukupna cena karata"))
        print("=" * 60)
        print ("{:<30} {:<30}".format(izvestaj[0], izvestaj[1]))
        print("=" * 60)
        input("Pritisnite bilo koji taster za nazad")

    def prikazi_izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za dan prodaje i prodavca")
                print("=" * 50)
                
                dan = input("Unesite datum prodaje(dd.mm.yyyy.): >>")

                try:
                    dan = datetime.strptime(dan, "%d.%m.%Y.").date()
                except ValueError:
                    raise Exception("dan prodaje nije odgovarajuceg formata")

                korsnicko_ime_prodavac = input("Unesite prodavca: >>")
                svi_korisnici = ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
                prodavac = svi_korisnici[korsnicko_ime_prodavac]

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                izvestaj = izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, svi_konkretni_letovi, svi_letovi, dan, prodavac)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<30} {:<30}".format("Ukupan broj karata", "Ukupna cena karata"))
        print("=" * 60)
        print ("{:<30} {:<30}".format(izvestaj[0], izvestaj[1]))
        print("=" * 60)
        input("Pritisnite bilo koji taster za nazad")

    def prikazi_izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima():
        uspesno = False
        while not uspesno:
            try:
                clear()
                print("=" * 50)
                print("Izvestaj prodatih karata za 30 dana po prodavcima")
                print("=" * 50)

                sve_karte = ucitaj_karte_iz_fajla("karte.csv", "|")
                svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
                svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
                izvestaj = izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi, svi_letovi)

                uspesno = True
            except Exception as message:
                user_input = None
                while user_input != "1" and user_input != "b":
                    clear()
                    print("Pogresni parametri!")
                    print(message)
                    print("1. Pokusajte ponovo")
                    print("b. nazad")
                    user_input = input(">>")
                    if user_input == "1":
                        continue
                    elif user_input == "b":
                        clear()
                        return
                    else:
                        clear()
                        print("uneli ste nepostojecu opciju")
                        input("Pritisnite enter za nazad")


        print("{:<30} {:<30} {:<30}".format("Prodavac" ,"Ukupan broj karata", "Ukupna cena karata"))
        print("=" * 90)
        for prodavac in izvestaj:
            print("{:<30} {:<30} {:<30}".format(prodavac, izvestaj[prodavac]["ukupno_karata"], izvestaj[prodavac]["ukupno_cena"]))
        print("=" * 90)
        input("Pritisnite bilo koji taster za nazad")


    menu_izvestaji_dict = {
        '1': prikazi_izvestaj_prodatih_karata_za_dan_prodaje,
        '2': prikazi_izvestaj_prodatih_karata_za_dan_polaska,
        '3': prikazi_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca,
        '4': prikazi_izvestaj_ubc_prodatih_karata_za_dan_prodaje,
        '5': prikazi_izvestaj_ubc_prodatih_karata_za_dan_polaska,
        '6': prikazi_izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca,
        '7': prikazi_izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima,
    }


    while True:
        clear()
        print("=" * 50)
        print("Meni generisanja izvestaja")
        print("=" * 50)
        
        print("Ponuđene opcije:")
        print("1. Lista prodatih karata za izabrani dan prodaje")
        print("2. Lista prodatih karata za izabrani dan polaska")
        print("3. Lista prodatih karata za izabrani dan prodaje i izabranog prodavca")
        print("4. Ukupan broj i cena prodatih karata za izabrani dan prodaje")
        print("5. Ukupan broj i cena prodatih karata za izabrani dan polaska")
        print("6. Ukupan broj i cena prodatih karata za izabrani dan prodaje i izabranog prodavca")
        print("7. Ukupan broj i cena prodatih karata u poslednjih 30 dana, po prodavcima")
    
        print("b. nazad")
        user_input = input(">>")

        if user_input in menu_izvestaji_dict:
            menu_izvestaji_dict[user_input]()
        elif user_input == "b":
            clear()
            return

        else:
            print("Odabrali ste nepostojeću opciju")
            input("Pritisnite enter za nazad")
