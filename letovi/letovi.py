from common import konstante
from datetime import datetime


"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    pass

"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    
    letovi = []

    if not isinstance(svi_letovi, dict):    
        raise Exception("Los unos")
        
    if not isinstance(konkretni_letovi, dict):    
        raise Exception("Los unos")

    for let in svi_letovi:
        if ((svi_letovi[let]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and 
            (svi_letovi[let]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste) and 
            (svi_letovi[let]["prevoznik"] == prevoznik or not prevoznik) and
            (svi_letovi[let]["vreme_poletanja"] == vreme_poletanja or not vreme_poletanja) and
            (svi_letovi[let]["vreme_sletanja"] == vreme_sletanja or not vreme_sletanja) 
            ):
            for konkretan_let in konkretni_letovi:
                if (
                    konkretni_letovi[konkretan_let]["broj_leta"] == let and 
                    (konkretni_letovi[konkretan_let]["datum_i_vreme_polaska"] == datum_polaska or not datum_polaska) and
                    (konkretni_letovi[konkretan_let]["datum_i_vreme_dolaska"] == datum_dolaska or not datum_dolaska)
                ):
                    letovi.append(konkretni_letovi[konkretan_let])
            
    return letovi

"""
Funkcija koja trazi 10 najjeftinijih letova po opadajucem redosledu
"""
def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    letovi = list((svi_letovi[key]["broj_leta"], svi_letovi[key]["cena"])
     for key in svi_letovi.keys()
     if (svi_letovi[key]["sifra_polazisnog_aerodroma"] == polaziste or not polaziste) and 
     (svi_letovi[key]["sifra_odredisnog_aerodorma"] == odrediste or not odrediste))

    letovi.sort(key = lambda k : k[1], reverse = True)

    return letovi[0:9]

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):



    if not isinstance(svi_letovi, dict):    
        raise Exception("Los unos")

    if not isinstance(broj_leta, str) or len(broj_leta) !=4 or not broj_leta[:2].isalpha() or not broj_leta[2:].isnumeric():       
        raise Exception("Los unos")

    if not isinstance(sifra_polazisnog_aerodroma, str) or len(sifra_polazisnog_aerodroma) != 3:    
        raise Exception("Los unos")

    if not isinstance(sifra_odredisnog_aerodorma, str) or len(sifra_odredisnog_aerodorma) != 3:    
        raise Exception("Los unos")

    if not isinstance(vreme_poletanja, str):    
       raise Exception("Los unos")

    try:    datetime.strptime(vreme_poletanja, "%H:%S")
    except ValueError:
        raise Exception("Los unos")


    if not isinstance(vreme_sletanja, str):    
        raise Exception("Los unos")


    try:    datetime.strptime(vreme_sletanja, "%H:%S")
    except ValueError:
        raise Exception("Los unos")


    if not isinstance(sletanje_sutra, bool):    
        raise Exception("Los unos")

    if not isinstance(prevoznik, str):    
        raise Exception("Los unos")

    if not isinstance(dani, list):    
        raise Exception("Los unos")

    if not isinstance(datum_pocetka_operativnosti, datetime):    
        raise Exception("Los unos")

    if not isinstance(datum_kraja_operativnosti, datetime):    
        raise Exception("Los unos")

    if not isinstance(model, dict):    
        raise Exception("Los unos")

    if not isinstance(cena, float):    
        raise Exception("Los unos")


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

        return svi_letovi        

    else:
        raise Exception(f"Los unos")

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

    if not isinstance(sifra_polazisnog_aerodroma, str) or len(sifra_polazisnog_aerodroma) != 3:    
        raise Exception("Los unos")

    if not isinstance(sifra_odredisnog_aerodorma, str) or len(sifra_odredisnog_aerodorma) != 3:    
        raise Exception("Los unos")

    if not isinstance(vreme_poletanja, str):    
        raise Exception("Los unos")

    try:    datetime.strptime(vreme_poletanja, "%H:%S")
    except ValueError:
        raise Exception("Los unos")

    if not isinstance(vreme_sletanja, str):    
        raise Exception("Los unos")

    try:    datetime.strptime(vreme_sletanja, "%H:%S")
    except ValueError:
        raise Exception("Los unos")


    if not isinstance(sletanje_sutra, bool):    
        raise Exception("Los unos")

    if not isinstance(prevoznik, str):    
        raise Exception("Los unos")

    if not isinstance(dani, list):    
        raise Exception("Los unos")

    if not isinstance(model, dict):    
        raise Exception("Los unos")

    if not isinstance(cena, float):    
        raise Exception("Los unos")

    if not isinstance(datum_pocetka_operativnosti, datetime):    
        raise Exception("Los unos")

    if not isinstance(datum_kraja_operativnosti, datetime):    
        raise Exception("Los unos")



    if broj_leta in svi_letovi:    
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

        return svi_letovi        

    else:
        raise Exception(f"Los unos")

"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    HEADERS_LISTA = konstante.PARAMETRI_LETA
    with open(putanja, "w") as f:
        for key in svi_letovi:    #prolazak kroz sve korisnike
            let_dict = svi_letovi[key]    #dictionary trenutnog korisnika
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(let_dict[parametar]))    #dodavanje parametara trenutnog korisnika u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(korisnika) u csv formatu
            f.write(linija+"\n")

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    ucitani_letovi = {}    
    HEADERS_LISTA = konstante.PARAMETRI_LETA
    with open(putanja, "r") as f:
        for let in f:    #prolazak kroz sve linije(korisnike)
            let = let.split(separator)    #korisnik je ovde lista sa vrednostima parametara korisnika
            let[-1] = let[-1][:-1]    #uklanjanje \n sa kraja linije
            
            let[HEADERS_LISTA.index("cena")] = float(let[HEADERS_LISTA.index("cena")])
            
            let[HEADERS_LISTA.index("dani")] = let[HEADERS_LISTA.index("dani")][1:-1].replace(" ", "").split(",")
            for i in range(len(let[HEADERS_LISTA.index("dani")])):
                let[HEADERS_LISTA.index("dani")][i] = int(let[HEADERS_LISTA.index("dani")][i])

            let[HEADERS_LISTA.index("model")] = eval(let[HEADERS_LISTA.index("model")])

            let[HEADERS_LISTA.index("datum_pocetka_operativnosti")] = datetime.strptime(let[HEADERS_LISTA.index("datum_pocetka_operativnosti")], "%Y-%m-%d %H:%M:%S")
            let[HEADERS_LISTA.index("datum_kraja_operativnosti")] = datetime.strptime(let[HEADERS_LISTA.index("datum_kraja_operativnosti")], "%Y-%m-%d %H:%M:%S")

            if let[HEADERS_LISTA.index("sletanje_sutra")] == "False":
                let[HEADERS_LISTA.index("sletanje_sutra")] = False
            elif let[HEADERS_LISTA.index("sletanje_sutra")] == "True":
                let[HEADERS_LISTA.index("sletanje_sutra")] = True
            else: raise Exception("Greska")

            ucitani_letovi[let[HEADERS_LISTA.index("broj_leta")]] = {}    #postavljanje kljuca na dictionary korisnika i pravljenje samog dictionary-a za korisnika 
            for parametar in HEADERS_LISTA:
                ucitani_letovi[let[HEADERS_LISTA.index("broj_leta")]][parametar] = let[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svakog korisnika u njegovom dictionary-u
    return ucitani_letovi    

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi, konkretan_let):
    matrica = []

    broj_redova = svi_letovi[konkretan_let["broj_leta"]]["model"]["broj_redova"]
    pozicije_sedenja = svi_letovi[konkretan_let["broj_leta"]]["model"]["pozicije_sedista"]
    
    sedista = []

    for i in range(len(pozicije_sedenja)):
        sedista.append(False)

    for i in range(broj_redova):
        matrica.append(sedista)

    konkretan_let["zauzetost"] = matrica

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretan_let):
    return konkretan_let["zauzetost"]