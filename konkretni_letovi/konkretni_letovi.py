from datetime import datetime, timedelta
from common import konstante
from letovi.letovi import podesi_matricu_zauzetosti, ucitaj_letove_iz_fajla

sledeca_sifra_konkretnog_leta = 1000

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    global sledeca_sifra_konkretnog_leta
    
    pocetak = let["datum_pocetka_operativnosti"]
    kraj = let["datum_kraja_operativnosti"]

    opseg = (kraj - pocetak).days

    vreme_poletanja = datetime.strptime(let["vreme_poletanja"], "%H:%M").time()
    vreme_sletanja = datetime.strptime(let["vreme_sletanja"], "%H:%M").time()

    dani = let["dani"]

    sletanje_sutra = let["sletanje_sutra"]

    for diff in range(opseg):
        datum_vreme = (pocetak + timedelta(days = diff))
        dan = datum_vreme.weekday()
        if dan in dani:
            if len(svi_konkretni_letovi.keys()) != 0: 
                sledeca_sifra_konkretnog_leta = max(svi_konkretni_letovi.keys()) + 1
            else:
                sledeca_sifra_konkretnog_leta = 1000

            sifra = sledeca_sifra_konkretnog_leta

            datum_konkretnog_leta = datum_vreme.date()
            

            svi_konkretni_letovi[sifra] = {}
            svi_konkretni_letovi[sifra]["sifra"] = sifra
            svi_konkretni_letovi[sifra]["broj_leta"] = let["broj_leta"]
            svi_konkretni_letovi[sifra]["datum_i_vreme_polaska"] = datetime.combine(datum_konkretnog_leta,vreme_poletanja)

            if sletanje_sutra:
                svi_konkretni_letovi[sifra]["datum_i_vreme_dolaska"] = datetime.combine(datum_konkretnog_leta,vreme_sletanja) + timedelta(days=1)
            else:
                svi_konkretni_letovi[sifra]["datum_i_vreme_dolaska"] = datetime.combine(datum_konkretnog_leta,vreme_sletanja)

            # svi_letovi = ucitaj_letove_iz_fajla("letovi.csv", "|")
            # svi_konkretni_letovi[sifra]["zauzetost"] = podesi_matricu_zauzetosti(svi_letovi, svi_konkretni_letovi[sifra])


    return svi_konkretni_letovi


"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    HEADERS_LISTA = konstante.PARAMETRI_KONKRETNOG_LETA
    with open(putanja, "w") as f:
        for key in svi_konkretni_letovi: 
            konkretan_let_dict = svi_konkretni_letovi[key]  
            linija_lista = []  
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(konkretan_let_dict[parametar]))   
            linija = separator.join(linija_lista)   
            f.write(linija+"\n")

"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    ucitani_konkretni_letovi = {}
    HEADERS_LISTA = konstante.PARAMETRI_KONKRETNOG_LETA
    with open(putanja, "r") as f:
        for konkretan_let in f:    
            konkretan_let = konkretan_let.split(separator)    
            konkretan_let[-1] = konkretan_let[-1][:-1]   

            konkretan_let[HEADERS_LISTA.index("sifra")] = int(konkretan_let[HEADERS_LISTA.index("sifra")])
            
            konkretan_let[HEADERS_LISTA.index("zauzetost")] = eval(konkretan_let[HEADERS_LISTA.index("zauzetost")])
    
            konkretan_let[HEADERS_LISTA.index("datum_i_vreme_polaska")] = datetime.strptime(konkretan_let[HEADERS_LISTA.index("datum_i_vreme_polaska")], "%Y-%m-%d %H:%M:%S")   
            konkretan_let[HEADERS_LISTA.index("datum_i_vreme_dolaska")] = datetime.strptime(konkretan_let[HEADERS_LISTA.index("datum_i_vreme_dolaska")], "%Y-%m-%d %H:%M:%S")  
            

            ucitani_konkretni_letovi[konkretan_let[HEADERS_LISTA.index("sifra")]] = {}   
            for parametar in HEADERS_LISTA:
                ucitani_konkretni_letovi[konkretan_let[HEADERS_LISTA.index("sifra")]][parametar] = konkretan_let[HEADERS_LISTA.index(parametar)] 

    return ucitani_konkretni_letovi