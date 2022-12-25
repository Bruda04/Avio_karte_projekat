from datetime import datetime, date
from functools import reduce


def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: datetime)->list:
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] == dan]
    return izvestaj
    
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date):
    izvesaj = [sve_karte[karta] for karta in sve_karte if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].date() == dan]
    return izvesaj

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str):
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] == dan and sve_karte[karta]["prodavac"] == prodavac]
    return izvestaj

def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] == dan:
            ukupan_broj += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return (ukupan_broj, ukupna_cena)

def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date): #ubc znaci ukupan broj i cena
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"] == dan: #!!!! treba da se ispravi na date
            ukupan_broj += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return (ukupan_broj, ukupna_cena)


def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str): #ubc znaci ukupan broj i cena
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] == dan and sve_karte[karta]["prodavac"] == prodavac:
            ukupan_broj += 1
            ukupna_cena += svi_letovi[konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
    return (ukupan_broj, ukupna_cena)

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict)->dict: #ubc znaci ukupan broj i cena
    izvestaj  = {}

    for karta in sve_karte:
        prodavac = sve_karte[karta]["prodavac"]
        if prodavac not in izvestaj:
            izvestaj[prodavac] = {"ukupno_karata": 0, "ukupno_cena": 0}
        elif prodavac in izvestaj and (sve_karte[karta]["datum_prodaje"]-datetime.now()).days <= 30:
            izvestaj[prodavac]["ukupno_karata"] += 1
            izvestaj[prodavac]["ukuono_cena"] += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return izvestaj
