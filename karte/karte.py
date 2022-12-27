from common import konstante
from datetime import datetime


"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
slesdeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs #prodavac i datum prodaje
) -> dict:
    global sledeci_broj_karte

    if len(sve_karte.keys()) != 0:  #postavljane sledeceg broja karte
        sledeci_broj_karte = max(sve_karte.keys()) + 1
    else:
        sledeci_broj_karte = 1

    try:
        prodavac = kwargs["prodavac"]
    except KeyError:
        pass

    try:
        datum_prodaje = kwargs["datum_prodaje"]
    except KeyError:
        pass

    if not isinstance(sve_karte, dict):
        raise Exception("Los unos")

    if not isinstance(svi_konkretni_letovi, dict):
        raise Exception("Los unos")

    if not isinstance(sifra_konkretnog_leta, int):
        raise Exception("Los unos")

    if not isinstance(putnici, list):
        raise Exception("Los unos")

    if not isinstance(slobodna_mesta, list):
        raise Exception("Los unos")

    if not isinstance(kupac, dict):
        raise Exception("Los unos")

    try:
        if not isinstance(prodavac, dict):
            raise Exception("Los unos")

        if not isinstance(datum_prodaje, datetime):
            raise Exception("Los unos")
    except NameError:
        pass

    if  sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("Greska")

    if kupac["uloga"] != konstante.ULOGA_KORISNIK:
        raise Exception("Greska")

    try:
        if prodavac["uloga"] != konstante.ULOGA_PRODAVAC:
            raise Exception("Greska")
    except NameError:
        pass


    ima_mesta = False

    for red in slobodna_mesta:      #provera da li ima mesta
        if ima_mesta:
            break
        for sediste in red:
            if not sediste:
                ima_mesta = True
                break


    # for red in range(len(slobodna_mesta)):
    #     if ima_mesta:
    #         break
    #     for sediste in range(len(slobodna_mesta[0])):
    #         if not slobodna_mesta[red][sediste]:
    #             ima_mesta = True
    #             novo_stanje = slobodna_mesta[red][:]
    #             novo_stanje[sediste] = True
    #             slobodna_mesta[red] = novo_stanje
    #             break
                
    if not ima_mesta:
        raise Exception("Greska")

    # svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"] = slobodna_mesta

    broj_karte = sledeci_broj_karte

    sve_karte[broj_karte] = {}
    sve_karte[broj_karte]["broj_karte"] = broj_karte
    sve_karte[broj_karte]["putnici"] = putnici
    sve_karte[broj_karte]["sifra_konkretnog_leta"] = sifra_konkretnog_leta
    sve_karte[broj_karte]["status"] = konstante.STATUS_NEREALIZOVANA_KARTA
    sve_karte[broj_karte]["obrisana"] = False
    sve_karte[broj_karte]["kupac"] = kupac      
    try:
        sve_karte[broj_karte]["datum_prodaje"] = datum_prodaje
        sve_karte[broj_karte]["prodavac"] = prodavac
    except NameError:
        pass


    return sve_karte[broj_karte]    

"""
Vraća sve nerealizovane karte za korisnika u listi.
"""
def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter) -> list:
    nerealizovane_karte = [karta for karta in sve_karte if karta["status"] == konstante.STATUS_NEREALIZOVANA_KARTA and korisnik in karta["putnici"]]    #prolazi kroz sve karte i uzima one sa validnom sttusom i putnicima
    return nerealizovane_karte

"""
Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata. Baca grešku ako podaci nisu validni.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]["obrisana"] = True
        return sve_karte
    elif korisnik["uloga"] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
        return sve_karte
    else:
        raise Exception("Greska")

"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    HEADERS_LISTA = konstante.PARAMETRI_KARATA
    with open(putanja, "w") as f:
        for key in sve_karte:    #prolazak kroz sve karte
            karta_dict = sve_karte[key]    #dictionary trenutne karte
            if not karta_dict["obrisana"]:
                linija_lista = []    #lista koja ce sadrzati parametre
                for parametar in HEADERS_LISTA:
                    linija_lista.append(str(karta_dict[parametar]))    #dodavanje parametara trenute karte u listu
                linija = separator.join(linija_lista)    #konverovanje liste u liniju(karte) u csv formatu
                f.write(linija+"\n")

"""
Funkcija koja učitava sve karte iz fajla i vraća ih u rečniku.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    ucitane_karte = {}
    HEADERS_LISTA = konstante.PARAMETRI_KARATA
    with open(putanja, "r") as f:
        for karta in f:    #prolazak kroz sve linije(karte)
            karta = karta.split(separator)    #karta je ovde lista sa vrednostima parametara karte
            karta[-1] = karta[-1][:-1]    #uklanjanje \n sa kraja linije

            karta[HEADERS_LISTA.index("broj_karte")] = int(karta[HEADERS_LISTA.index("broj_karte")])
            karta[HEADERS_LISTA.index("sifra_konkretnog_leta")] = int(karta[HEADERS_LISTA.index("sifra_konkretnog_leta")])

            if karta[HEADERS_LISTA.index("obrisana")] == "False":
                karta[HEADERS_LISTA.index("obrisana")] = False
            elif karta[HEADERS_LISTA.index("obrisana")] == "True":
                karta[HEADERS_LISTA.index("obrisana")] = True
            else: raise Exception("Greska")



            ucitane_karte[karta[HEADERS_LISTA.index("broj_karte")]] = {}    #postavljanje kljuca na dictionary karte i pravljenje samog dictionary-a za kartu
            for parametar in HEADERS_LISTA:
                ucitane_karte[karta[HEADERS_LISTA.index("broj_karte")]][parametar] = karta[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaku kartu u njenom dictionary-u

    return ucitane_karte