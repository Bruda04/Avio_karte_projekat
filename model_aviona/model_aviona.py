from common import konstante


sledeci_model_id = 0

"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicije_sedista: list = []
) -> dict:
    global sledeci_model_id

    if len(svi_modeli_aviona.keys()) != 0:  #postavljane sledeceg broja karte
        sledeci_model_id = max(svi_modeli_aviona.keys()) + 1
    else:
        sledeci_model_id = 0

    if not isinstance(svi_modeli_aviona, dict):    
        raise Exception("svi_modeli_aviona nije oblika dict")

    if not isinstance(naziv, str) or not naziv:    
        raise Exception("naziv nije oblika str")

    if not isinstance(broj_redova, int) or not broj_redova:    
        raise Exception("broj redova nije oblika str")

    if not isinstance(pozicije_sedista, list) or not pozicije_sedista:    
        raise Exception("pozicija sedista nije oblika str")

    id  = sledeci_model_id

    if id not in svi_modeli_aviona:    
        svi_modeli_aviona[id] = {}
        svi_modeli_aviona[id]["id"] = id
        svi_modeli_aviona[id]["naziv"] = naziv
        svi_modeli_aviona[id]["broj_redova"] = broj_redova
        svi_modeli_aviona[id]["pozicije_sedista"] = pozicije_sedista

        return svi_modeli_aviona        

    else:
        raise Exception("model vec postoji")


"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_modeli_aviona: dict):
    HEADERS_LISTA = konstante.PARAMETRI_MODELA
    with open(putanja, "w") as f:
        for key in svi_modeli_aviona:    #prolazak kroz sve letove
            modeli_dict = svi_modeli_aviona[key]    #dictionary trenutnog leta
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(modeli_dict[parametar]))    #dodavanje parametara trenutnog leta u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(let) u csv formatu
            f.write(linija+"\n")


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    ucitani_modeli = {}    
    HEADERS_LISTA = konstante.PARAMETRI_MODELA
    with open(putanja, "r") as f:
        for model in f:    #prolazak kroz sve linije(aerodromove)
            model = model.split(separator)    #aerodrom je ovde lista sa vrednostima parametara aerodroma
            model[-1] = model[-1][:-1]    #uklanjanje \n sa kraja linije

            model[HEADERS_LISTA.index("id")] = int(model[HEADERS_LISTA.index("id")])

            model[HEADERS_LISTA.index("broj_redova")] = int(model[HEADERS_LISTA.index("broj_redova")])

            model[HEADERS_LISTA.index("pozicije_sedista")] = eval(model[HEADERS_LISTA.index("pozicije_sedista")])

            ucitani_modeli[model[HEADERS_LISTA.index("id")]] = {}    #postavljanje kljuca na dictionary aerodroma i pravljenje samog dictionary-a za aerodrom 
            for parametar in HEADERS_LISTA:
                ucitani_modeli[model[HEADERS_LISTA.index("id")]][parametar] = model[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaki aerodrom u njegovom dictionary-u
    return ucitani_modeli
