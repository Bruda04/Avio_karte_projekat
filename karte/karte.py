from common import konstante
from datetime import datetime


"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

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
    **kwargs
) -> dict: #-> (dict, dict)
    global sledeci_broj_karte

    if len(sve_karte.keys()) != 0:  #postavljane sledeceg broja karte
        sledeci_broj_karte = max(sve_karte.keys()) + 1
    else:
        sledeci_broj_karte = 1


    prodavac = ""
    datum_prodaje = ""

    if "prodavac" in kwargs:
        prodavac = kwargs["prodavac"]
    if "datum_prodaje" in kwargs:
        datum_prodaje = kwargs["datum_prodaje"]

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


    if prodavac != "" and not isinstance(prodavac, dict):
        raise Exception("Los unos")

    if datum_prodaje != "" and not isinstance(datum_prodaje, datetime):
        raise Exception("Los unos")
 
    if  sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("Greska")

    if kupac["uloga"] != konstante.ULOGA_KORISNIK:
        raise Exception("Greska")

    if prodavac and prodavac["uloga"] != konstante.ULOGA_PRODAVAC:
        raise Exception("Greska")



    ima_mesta = False

    for red in slobodna_mesta:      #provera da li ima mesta
        if ima_mesta:
            break
        for sediste in red:
            if not sediste:
                ima_mesta = True
                break
    
    if not ima_mesta:
        raise Exception("Nema mesta")

    broj_karte = sledeci_broj_karte

    sve_karte[broj_karte] = {}
    sve_karte[broj_karte]["broj_karte"] = broj_karte
    sve_karte[broj_karte]["putnici"] = putnici
    sve_karte[broj_karte]["sifra_konkretnog_leta"] = sifra_konkretnog_leta
    sve_karte[broj_karte]["status"] = konstante.STATUS_NEREALIZOVANA_KARTA
    sve_karte[broj_karte]["obrisana"] = False
    sve_karte[broj_karte]["kupac"] = kupac      
    sve_karte[broj_karte]["datum_prodaje"] = datum_prodaje
    sve_karte[broj_karte]["prodavac"] = prodavac



    return (sve_karte[broj_karte], sve_karte) 

"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska: datetime=None,
    sediste=None
) -> dict:

    if not isinstance(sve_karte, dict):
        raise Exception("Los unos")

    if not isinstance(svi_konkretni_letovi, dict):
        raise Exception("Los unos")

    # if nova_sifra_konkretnog_leta not in svi_konkretni_letovi:
    #     raise Exception("Ne postoji uneta sifra konkretnog leta")

    sve_karte[broj_karte]["sifra_konkretnog_leta"] = nova_sifra_konkretnog_leta
    sve_karte[broj_karte]["datum_prodaje"] = nov_datum_polaska
    sve_karte[broj_karte]["sediste"] = sediste
 

    return sve_karte 

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
Kao rezultat se vraća nova kolekcija svih karata.
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
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: str="",
                             korisnicko_ime_putnika: str="")->list:
    karte = []

    if not isinstance(svi_letovi, dict):    #porvera oblika svi_letovi
        raise Exception("Svi_letovi nije oblika dict")
        
    if not isinstance(svi_konkretni_letovi, dict):    #porvera oblika konkretni_letovi
        raise Exception("konkretni_letovi nije oblika dict")
        
    if not isinstance(sve_karte, dict):    #porvera oblika konkretni_letovi
        raise Exception("sve_karte nije oblika dict")

    for karta in sve_karte:
        konkretan_let  = svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]
        let = svi_letovi[konkretan_let["broj_leta"]]
        
        if (
            (let["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and    #da li su parametri uneti i odgovarajuci ili nisu uneti
            (let["sifra_odredisnog_aerodorma"] == odrediste or not odrediste) and 
            (konkretan_let["datum_i_vreme_polaska"] == datum_polaska or not datum_polaska) and
            (konkretan_let["datum_i_vreme_dolaska"] == datum_dolaska or not datum_dolaska)
            ):
                for putnik in sve_karte[karta]["putnici"]:
                    if korisnicko_ime_putnika == putnik["korisnicko_ime"] or not korisnicko_ime_putnika:
                        if sve_karte[karta] not in karte:
                            karte.append(sve_karte[karta])      #dodaj let u povratnu listu ako je prosao sve provere
        
    return karte

"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    HEADERS_LISTA = konstante.PARAMETRI_KARATA
    with open(putanja, "w") as f:
        for key in sve_karte:    #prolazak kroz sve karte

            karta_dict = sve_karte[key]    #dictionary trenutne karte
            if "sediste" not in karta_dict:
                karta_dict["sediste"] = ""
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(karta_dict[parametar]))    #dodavanje parametara trenute karte u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(karte) u csv formatu
            f.write(linija+"\n")

"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
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

            if karta[HEADERS_LISTA.index("datum_prodaje")] != "":
                karta[HEADERS_LISTA.index("datum_prodaje")] = datetime.strptime(karta[HEADERS_LISTA.index("datum_prodaje")], "%Y-%m-%d %H:%M:%S")

            karta[HEADERS_LISTA.index("putnici")] = eval(karta[HEADERS_LISTA.index("putnici")])
            karta[HEADERS_LISTA.index("kupac")] = eval(karta[HEADERS_LISTA.index("kupac")])
            if karta[HEADERS_LISTA.index("prodavac")] != "":
                karta[HEADERS_LISTA.index("prodavac")] = eval(karta[HEADERS_LISTA.index("prodavac")])


            ucitane_karte[karta[HEADERS_LISTA.index("broj_karte")]] = {}    #postavljanje kljuca na dictionary karte i pravljenje samog dictionary-a za kartu
            for parametar in HEADERS_LISTA:
                ucitane_karte[karta[HEADERS_LISTA.index("broj_karte")]][parametar] = karta[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaku kartu u njenom dictionary-u

    return ucitane_karte

