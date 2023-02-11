from common import konstante
from datetime import datetime, date, timedelta
#from konkretni_letovi.konkretni_letovi import kreiranje_konkretnog_leta, sacuvaj_kokretan_let, ucitaj_konkretan_let

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizoivanih_letova(svi_letovi: dict):
    letovi = [svi_letovi[let] for let in svi_letovi if svi_letovi[let]["datum_pocetka_operativnosti"] >= datetime.now()]
    return letovi

"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    letovi = []

    if not isinstance(svi_letovi, dict):    #porvera oblika svi_letovi
        raise Exception("Svi_letovi nije oblika dict")
        
    if not isinstance(konkretni_letovi, dict):    #porvera oblika konkretni_letovi
        raise Exception("konkretni_letovi nije oblika dict")

    for let in svi_letovi:
        if ((svi_letovi[let]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and    #da li su parametri uneti i odgovarajuci ili nisu uneti
            (svi_letovi[let]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste) and 
            (svi_letovi[let]["prevoznik"] == prevoznik or not prevoznik) and
            (svi_letovi[let]["vreme_poletanja"] == vreme_poletanja or not vreme_poletanja) and
            (svi_letovi[let]["vreme_sletanja"] == vreme_sletanja or not vreme_sletanja) 
            ):
            for konkretan_let in konkretni_letovi:
                if (
                    konkretni_letovi[konkretan_let]["broj_leta"] == let and 
                    (not datum_polaska or konkretni_letovi[konkretan_let]["datum_i_vreme_polaska"].date() == datum_polaska.date()) and
                    (not datum_dolaska or konkretni_letovi[konkretan_let]["datum_i_vreme_dolaska"].date() == datum_dolaska.date())
                ):
                    letovi.append(konkretni_letovi[konkretan_let])      #dodaj let u povratnu listu ako je prosao sve provere
            
    return letovi

"""
Funkcija koja trazi 10 najjeftinijih letova po opadajucem redosledu
"""
def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    odgovarajuci = 0
    for let in svi_letovi:
        if (
        (svi_letovi[let]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and 
        (svi_letovi[let]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste)
        ):
            odgovarajuci +=1 
    if odgovarajuci == 0:
        raise Exception("Nema odgovarjucih letova")
    
    letovi = list((svi_letovi[key])       #vraca broj leta i cenu tuple
     for key in svi_letovi.keys()
     if (svi_letovi[key]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and       #za odgovarajuce polaziste i odrediste
     (svi_letovi[key]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste))


    letovi.sort(key = lambda k : k["cena"], reverse=True)      #sortiranje po lambda funkciji koja izvlaci parametar cena
    return letovi[-10:]      #vracanje poslednjih 10

    # letovi.sort(key = lambda k : k["cena"])      #sortiranje po lambda funkciji koja izvlaci parametar cena
    # return letovi[:9]      #vracanje poslednjih 10

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):
    if not isinstance(svi_letovi, dict):    
        raise Exception("svi_letovi nije oblika dict")

    if not isinstance(broj_leta, str) or len(broj_leta) != 4 or not broj_leta[:2].isalpha() or not broj_leta[2:].isnumeric():       
        raise Exception("broj_leta nije oblika str ili nije odgovarajuceg oblika")

    if not isinstance(sifra_polazisnog_aerodroma, str) or len(sifra_polazisnog_aerodroma) != 3 or not sifra_polazisnog_aerodroma.isalpha():    
        raise Exception("sifra_polazisnog_aerodroma nije str ili nije odogovarajuceg oblika")

    if not isinstance(sifra_odredisnog_aerodorma, str) or len(sifra_odredisnog_aerodorma) != 3 or not sifra_odredisnog_aerodorma.isalpha():    
        raise Exception("sifra_odredisnog_aerodorma nije str ili nije odogovarajuceg oblika")

    if not isinstance(vreme_poletanja, str):    
       raise Exception("vreme_poletanja nije oblika str")

    try:    datetime.strptime(vreme_poletanja, "%H:%M")     #Provera da li prosledjeno vreme moze da se pretvori u odgovarajuci oblik
    except ValueError:
        raise Exception("vreme_poletanja nije odgovarajuceg formata")


    if not isinstance(vreme_sletanja, str):    
        raise Exception("vreme_sletanja nije odgovarajuceg formata")


    try:    datetime.strptime(vreme_sletanja, "%H:%M")      #Provera da li prosledjeno vreme moze da se pretvori u odgovarajuci oblik
    except ValueError:
        raise Exception("Vreme sletanja nije dobrog formata")


    if not isinstance(sletanje_sutra, bool):    
        raise Exception("Sletanje sutra nije validnog formata")

    if not isinstance(prevoznik, str) or not prevoznik:    
        raise Exception("Prevoznik nije lepo unet")

    if not isinstance(dani, list) or len(dani) == 0:    
        raise Exception("Dani nisu lista")

    if not isinstance(datum_pocetka_operativnosti, datetime):    
        raise Exception("Datum pocetka operativnosti nije dobrog formata")

    if not isinstance(datum_kraja_operativnosti, datetime):    
        raise Exception("Datum kraja operativnosti nije dobrog formata")

    if not isinstance(model, dict) or len(model) == 0:     
        raise Exception("Nema tog modela aviona")

    if not isinstance(cena, float):    
        raise Exception("Cena mora biti float")

    if datum_pocetka_operativnosti >= datum_kraja_operativnosti:
        raise Exception("kraj operativnost ne moze biti pre pocetka operativnosti")


    if broj_leta not in svi_letovi:    
        svi_letovi[broj_leta] = {}
        svi_letovi[broj_leta]["broj_leta"] = broj_leta
        svi_letovi[broj_leta]["sifra_polazisnog_aerodroma"] = sifra_polazisnog_aerodroma
        svi_letovi[broj_leta]["sifra_odredisnog_aerodorma"] = sifra_odredisnog_aerodorma
        svi_letovi[broj_leta]["vreme_poletanja"] = vreme_poletanja
        svi_letovi[broj_leta]["vreme_sletanja"] = vreme_sletanja
        svi_letovi[broj_leta]["sletanje_sutra"] = sletanje_sutra
        svi_letovi[broj_leta]["prevoznik"] = prevoznik
        svi_letovi[broj_leta]["dani"] = dani
        svi_letovi[broj_leta]["datum_pocetka_operativnosti"] = datum_pocetka_operativnosti
        svi_letovi[broj_leta]["datum_kraja_operativnosti"] = datum_kraja_operativnosti 
        svi_letovi[broj_leta]["model"] = model
        svi_letovi[broj_leta]["cena"] = cena
        
        # svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
        # novi_konkretni_letovi = kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
        # sacuvaj_kokretan_let("konkretni_letovi.csv", "|", novi_konkretni_letovi)

        return svi_letovi        

    else:
        raise Exception(f"Broj leta vec postoji")

"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float, datum_pocetka_operativnosti: datetime,
                     datum_kraja_operativnosti: datetime)-> dict:
    
    if not isinstance(svi_letovi, dict):    
        raise Exception("Los unos")

    if not isinstance(broj_leta, str) or len(broj_leta)!=4 or not broj_leta[:2].isalpha() or not broj_leta[2:].isnumeric():    
        print(broj_leta[:2] , broj_leta[2:])
        raise Exception("Los unos")

    if not isinstance(sifra_polazisnog_aerodroma, str) or len(sifra_polazisnog_aerodroma) != 3 or not sifra_polazisnog_aerodroma.isalpha():    
        raise Exception("Los unos")

    if not isinstance(sifra_odredisnog_aerodorma, str) or len(sifra_odredisnog_aerodorma) != 3 or not sifra_odredisnog_aerodorma.isalpha():    
        raise Exception("Los unos")

    if not isinstance(vreme_poletanja, str):    
        raise Exception("Los unos")

    try:    datetime.strptime(vreme_poletanja, "%H:%M")
    except ValueError:
        raise Exception("Los unos")

    if not isinstance(vreme_sletanja, str):    
        raise Exception("Los unos")

    try:    datetime.strptime(vreme_sletanja, "%H:%M")
    except ValueError:
        raise Exception("Los unos")


    if not isinstance(sletanje_sutra, bool):    
        raise Exception("Los unos")

    if not isinstance(prevoznik, str) or not prevoznik:    
        raise Exception("Los unos")

    if not isinstance(dani, list) or len(dani) == 0:    
        raise Exception("Los unos")

    if not isinstance(model, dict) or len(model) == 0:    
        raise Exception("Los unos")

    if not isinstance(cena, float):    
        raise Exception("Los unos")

    if not isinstance(datum_pocetka_operativnosti, datetime):    
        raise Exception("Los unos")

    if not isinstance(datum_kraja_operativnosti, datetime):    
        raise Exception("Los unos")

    if datum_pocetka_operativnosti >= datum_kraja_operativnosti:
        raise Exception("kraj operativnost ne moze biti pre pocetka operativnosti")


    if broj_leta in svi_letovi:    
        svi_letovi[broj_leta]["sifra_polazisnog_aerodroma"] = sifra_polazisnog_aerodroma
        svi_letovi[broj_leta]["sifra_odredisnog_aerodorma"] = sifra_odredisnog_aerodorma
        svi_letovi[broj_leta]["vreme_poletanja"] = vreme_poletanja
        svi_letovi[broj_leta]["vreme_sletanja"] = vreme_sletanja
        svi_letovi[broj_leta]["sletanje_sutra"] = sletanje_sutra
        svi_letovi[broj_leta]["prevoznik"] = prevoznik
        svi_letovi[broj_leta]["dani"] = dani
        svi_letovi[broj_leta]["datum_pocetka_operativnosti"] = datum_pocetka_operativnosti
        svi_letovi[broj_leta]["datum_kraja_operativnosti"] = datum_kraja_operativnosti 
        svi_letovi[broj_leta]["model"] = model
        svi_letovi[broj_leta]["cena"] = cena

        # svi_konkretni_letovi = ucitaj_konkretan_let("konkretni_letovi.csv", "|")
        # svi_konkretni_letovi_copy = {}
        
        # for konkretan_let in svi_konkretni_letovi:
        #     if svi_konkretni_letovi[konkretan_let]["broj_leta"] != broj_leta:
        #         # del svi_konkretni_letovi_copy[konkretan_let]
        #         svi_konkretni_letovi_copy[konkretan_let] = svi_konkretni_letovi[konkretan_let]

        # novi_konkretni_letovi = kreiranje_konkretnog_leta(svi_konkretni_letovi_copy, svi_letovi[broj_leta])
        # sacuvaj_kokretan_let("konkretni_letovi.csv", "|", novi_konkretni_letovi)

        return svi_letovi        

    else:
        raise Exception(f"Los unos")

"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    HEADERS_LISTA = konstante.PARAMETRI_LETA
    with open(putanja, "w") as f:
        for key in svi_letovi:    #prolazak kroz sve letove
            let_dict = svi_letovi[key]    #dictionary trenutnog leta
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(let_dict[parametar]))    #dodavanje parametara trenutnog leta u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(let) u csv formatu
            f.write(linija+"\n")

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    ucitani_letovi = {}    
    HEADERS_LISTA = konstante.PARAMETRI_LETA
    with open(putanja, "r") as f:
        for let in f:    #prolazak kroz sve linije(letove)
            let = let.split(separator)    #let je ovde lista sa vrednostima parametara leta
            let[-1] = let[-1][:-1]    #uklanjanje \n sa kraja linije
            
            let[HEADERS_LISTA.index("cena")] = float(let[HEADERS_LISTA.index("cena")])      #konvertovanje cene u float
            
            let[HEADERS_LISTA.index("dani")] = let[HEADERS_LISTA.index("dani")][1:-1].replace(" ", "").split(",")   #uklanjanje razmaka i zagrada i splitovanje po , 
            for i in range(len(let[HEADERS_LISTA.index("dani")])):
                let[HEADERS_LISTA.index("dani")][i] = int(let[HEADERS_LISTA.index("dani")][i])      #konvertovanje svih dana u int

            let[HEADERS_LISTA.index("model")] = eval(let[HEADERS_LISTA.index("model")])     #pretvaranje modela u dict

            let[HEADERS_LISTA.index("datum_pocetka_operativnosti")] = datetime.strptime(let[HEADERS_LISTA.index("datum_pocetka_operativnosti")], "%Y-%m-%d %H:%M:%S")   #kovertovfanje iz str formata u datetime
            let[HEADERS_LISTA.index("datum_kraja_operativnosti")] = datetime.strptime(let[HEADERS_LISTA.index("datum_kraja_operativnosti")], "%Y-%m-%d %H:%M:%S")

            if let[HEADERS_LISTA.index("sletanje_sutra")] == "False":
                let[HEADERS_LISTA.index("sletanje_sutra")] = False
            elif let[HEADERS_LISTA.index("sletanje_sutra")] == "True":
                let[HEADERS_LISTA.index("sletanje_sutra")] = True
            else: raise Exception("Greska")

            ucitani_letovi[let[HEADERS_LISTA.index("broj_leta")]] = {}    #postavljanje kljuca na dictionary leta i pravljenje samog dictionary-a za let 
            for parametar in HEADERS_LISTA:
                ucitani_letovi[let[HEADERS_LISTA.index("broj_leta")]][parametar] = let[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaki let u njegovom dictionary-u
    return ucitani_letovi    

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi, konkretan_let):
    matrica = []

    broj_redova = svi_letovi[konkretan_let["broj_leta"]]["model"]["broj_redova"]    #dobavljanje broja redova za matricu
    pozicije_sedenja = svi_letovi[konkretan_let["broj_leta"]]["model"]["pozicije_sedista"]  #dobavljanje broja kolona za matricu
    
    sedista = []

    for i in range(len(pozicije_sedenja)):
        sedista.append(False)   #pravljenje kolone sa False parametrima

    for i in range(broj_redova):
        matrica.append(sedista)     #dodavanje redova u matricu

    konkretan_let["zauzetost"] = matrica    #postavljanje matrice na parametar zauzetost

    return matrica

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretan_let):
    return konkretan_let["zauzetost"]

"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> dict: #(dict, dict)
    rok = 48
    matrica = matrica_zauzetosti(konkretni_let)
    broj_leta = konkretni_let["broj_leta"]
    let  = svi_letovi[broj_leta]
    model = let["model"]
    vreme_poletanja = konkretni_let["datum_i_vreme_polaska"]

    if datetime.now() > vreme_poletanja - timedelta(hours = rok):
        raise Exception("Prosao je rok za checkin")
    
    if red-1 > model["broj_redova"] or pozicija not in model["pozicije_sedista"]:
        raise Exception("Nevalidan pozicija")

    kolona = model["pozicije_sedista"].index(pozicija)

    if matrica[red-1][kolona]:
        raise Exception("Mesto zauzeto")
    
    matrica[red-1][kolona] = True

    konkretni_let["zauzetost"] = matrica
    karta["status"] = konstante.STATUS_REALIZOVANA_KARTA
    sediste = pozicija + str(red)
    karta["sediste"] = sediste

    return (konkretni_let, karta)

"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    if konkretni_let not in svi_konkretni_letovi.values() or konkretni_let["broj_leta"] not in svi_letovi:
        raise Exception("Nepostoji prosledjeni konkretni let")
    
    mesto_presedanja = svi_letovi[konkretni_let["broj_leta"]]["sifra_odredisnog_aerodorma"]

    letovi = [svi_konkretni_letovi[konkretno] for konkretno in svi_konkretni_letovi if 
    (svi_letovi[svi_konkretni_letovi[konkretno]["broj_leta"]]["sifra_polazisnog_aerodroma"]) == mesto_presedanja and
    ((konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=120)) >= svi_konkretni_letovi[konkretno]["datum_i_vreme_polaska"]) and 
    (konkretni_let["datum_i_vreme_dolaska"] <= svi_konkretni_letovi[konkretno]["datum_i_vreme_polaska"])]
    
    if len(letovi) == 0:
        raise Exception("Nije pronadjen odgovarjuci povezani let")
    return letovi

"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    
    if not isinstance(svi_letovi, dict):    #porvera oblika svi_letovi
        raise Exception("Svi_letovi nije oblika dict")
        
    if not isinstance(konkretni_letovi, dict):    #porvera oblika konkretni_letovi
        raise Exception("konkretni_letovi nije oblika dict")

    if not isinstance(datum_dolaska, datetime):    #porvera oblika konkretni_letovi
        raise Exception("datum_dolaska nije oblika dd.mm.yyyy.")

    if not isinstance(datum_polaska, datetime):    #porvera oblika konkretni_letovi
        raise Exception("datum_polaska nije oblika dd.mm.yyyy.")

    
    
    letovi = []
    

    polazak_min = datum_polaska - timedelta(days=broj_fleksibilnih_dana)
    polazak_max = datum_polaska + timedelta(days=broj_fleksibilnih_dana)
    dolazak_min = datum_dolaska - timedelta(days=broj_fleksibilnih_dana)
    dolazak_max = datum_dolaska + timedelta(days=broj_fleksibilnih_dana)


    for let in svi_letovi:
        if ((svi_letovi[let]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and    #da li su parametri uneti i odgovarajuci ili nisu uneti
            (svi_letovi[let]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste)
            ):
            for konkretan_let in konkretni_letovi:
                if (
                    konkretni_letovi[konkretan_let]["broj_leta"] == let and 
                    ((konkretni_letovi[konkretan_let]["datum_i_vreme_polaska"] >= polazak_min and konkretni_letovi[konkretan_let]["datum_i_vreme_polaska"] <= polazak_max) or not datum_polaska) and
                    ((konkretni_letovi[konkretan_let]["datum_i_vreme_dolaska"] >= dolazak_min and konkretni_letovi[konkretan_let]["datum_i_vreme_dolaska"] <= dolazak_max) or not datum_dolaska)
                ):
                    letovi.append(konkretni_letovi[konkretan_let])      #dodaj let u povratnu listu ako je prosao sve provere
            
    return letovi
