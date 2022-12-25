from datetime import datetime, timedelta
from common import konstante

sledeca_sifra_konkretnog_leta = 1000

def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):
    global sledeca_sifra_konkretnog_leta
    
    pocetak = let["datum_pocetka_operativnosti"]
    kraj = let["datum_kraja_operativnosti"]

    opseg = (kraj - pocetak).days

    vreme_poletanja = datetime.strptime(let["vreme_poletanja"], "%H:%M").time()
    vreme_sletanja = datetime.strptime(let["vreme_sletanja"], "%H:%M").time()

    dani = let["dani"]

    for diff in range(opseg):
        datum_vreme = (pocetak + timedelta(days = diff))
        dan = datum_vreme.weekday()
        if dan in dani:
            if len(svi_konkretni_letovi.keys()) != 0:  #postavljane sledeceg broja karte
                sledeca_sifra_konkretnog_leta = max(svi_konkretni_letovi.keys()) + 1
            else:
                sledeca_sifra_konkretnog_leta = 1000

            sifra = sledeca_sifra_konkretnog_leta

            datum_konkretnog_leta = datum_vreme.date()
            

            svi_konkretni_letovi[sifra] = {}
            svi_konkretni_letovi[sifra]["sifra"] = sifra
            svi_konkretni_letovi[sifra]["broj_leta"] = let["broj_leta"]
            svi_konkretni_letovi[sifra]["datum_i_vreme_polaska"] = datetime.combine(datum_konkretnog_leta,vreme_poletanja)
            svi_konkretni_letovi[sifra]["datum_i_vreme_dolaska"] = datetime.combine(datum_konkretnog_leta,vreme_sletanja)
        


    return svi_konkretni_letovi

def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    HEADERS_LISTA = konstante.PARAMETRI_KONKRETNOG_LETA
    with open(putanja, "w") as f:
        for key in svi_konkretni_letovi:    #prolazak kroz sve letove
            konkretan_let_dict = svi_konkretni_letovi[key]    #dictionary trenutnog leta
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(konkretan_let_dict[parametar]))    #dodavanje parametara trenutnog leta u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(let) u csv formatu
            f.write(linija+"\n")

def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    ucitani_konkretni_letovi = {}
    HEADERS_LISTA = konstante.PARAMETRI_KONKRETNOG_LETA
    with open(putanja, "r") as f:
        for konkretan_let in f:    #prolazak kroz sve linije(karte)
            konkretan_let = konkretan_let.split(separator)    #karta je ovde lista sa vrednostima parametara karte
            konkretan_let[-1] = konkretan_let[-1][:-1]    #uklanjanje \n sa kraja linije

            konkretan_let[HEADERS_LISTA.index("sifra")] = int(konkretan_let[HEADERS_LISTA.index("sifra")])
    
            konkretan_let[HEADERS_LISTA.index("datum_i_vreme_polaska")] = datetime.strptime(konkretan_let[HEADERS_LISTA.index("datum_i_vreme_polaska")], "%Y-%m-%d %H:%M:%S")   #kovertovfanje iz str formata u datetime
            konkretan_let[HEADERS_LISTA.index("datum_i_vreme_dolaska")] = datetime.strptime(konkretan_let[HEADERS_LISTA.index("datum_i_vreme_dolaska")], "%Y-%m-%d %H:%M:%S")   #kovertovfanje iz str formata u datetime
            

            ucitani_konkretni_letovi[konkretan_let[HEADERS_LISTA.index("sifra")]] = {}    #postavljanje kljuca na dictionary karte i pravljenje samog dictionary-a za kartu
            for parametar in HEADERS_LISTA:
                ucitani_konkretni_letovi[konkretan_let[HEADERS_LISTA.index("sifra")]][parametar] = konkretan_let[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaku kartu u njenom dictionary-u
    return ucitani_konkretni_letovi
