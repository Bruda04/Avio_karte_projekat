from datetime import datetime


def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: str)->list:
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] == dan]
    return izvestaj
    

def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: str):
    pass

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: str, prodavac: str):
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] == dan and sve_karte[karta]["prodavac"] == prodavac]
    pass

def izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte: dict, svi_konkretni_letovi, dan: str): #ubc znaci ukupan broj i cena vraca neki tapl
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] == dan:
            ukupan_broj += 1
    return (ukupan_broj, ukupna_cena)

def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: str): #ubc znaci ukupan broj i cena
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"] == dan:
            ukupan_broj += 1
    return (ukupan_broj, ukupna_cena)


def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: str, prodavac: str): #ubc znaci ukupan broj i cena
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] == dan and sve_karte[karta]["prodavac"] == prodavac:
            ukupan_broj += 1
    return (ukupan_broj, ukupna_cena)

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict)->dict: #ubc znaci ukupan broj i cena
    pass


