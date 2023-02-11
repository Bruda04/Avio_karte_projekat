from common import konstante


"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    if not isinstance(svi_aerodromi, dict):    
        raise Exception("svi_aerodromi nije oblika dict")

    if not isinstance(skracenica, str) or not skracenica:    
        raise Exception("skracenica nije oblika str")

    if not isinstance(pun_naziv, str) or not pun_naziv:    
        raise Exception("pun naziv nije oblika str")

    if not isinstance(grad, str) or not grad:    
        raise Exception("grad nije oblika str")

    if not isinstance(drzava, str) or not drzava:    
        raise Exception("drzava nije oblika str")


    if skracenica not in svi_aerodromi:    
        svi_aerodromi[skracenica] = {}
        svi_aerodromi[skracenica]["skracenica"] = skracenica
        svi_aerodromi[skracenica]["pun_naziv"] = pun_naziv
        svi_aerodromi[skracenica]["grad"] = grad
        svi_aerodromi[skracenica]["drzava"] = drzava

        return svi_aerodromi        

    else:
        raise Exception("Aerodrom vec postoji")

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    HEADERS_LISTA = konstante.PARAMETRI_AERODROMA
    with open(putanja, "w") as f:
        for key in svi_aerodromi:    #prolazak kroz sve letove
            aerodrom_dict = svi_aerodromi[key]    #dictionary trenutnog leta
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(str(aerodrom_dict[parametar]))    #dodavanje parametara trenutnog leta u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(let) u csv formatu
            f.write(linija+"\n")

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    ucitani_aerodromi = {}    
    HEADERS_LISTA = konstante.PARAMETRI_AERODROMA
    with open(putanja, "r") as f:
        for aerodrom in f:    #prolazak kroz sve linije(aerodromove)
            aerodrom = aerodrom.split(separator)    #aerodrom je ovde lista sa vrednostima parametara aerodroma
            aerodrom[-1] = aerodrom[-1][:-1]    #uklanjanje \n sa kraja linije

            ucitani_aerodromi[aerodrom[HEADERS_LISTA.index("skracenica")]] = {}    #postavljanje kljuca na dictionary aerodroma i pravljenje samog dictionary-a za aerodrom 
            for parametar in HEADERS_LISTA:
                ucitani_aerodromi[aerodrom[HEADERS_LISTA.index("skracenica")]][parametar] = aerodrom[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svaki aerodrom u njegovom dictionary-u
    return ucitani_aerodromi 
