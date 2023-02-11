from datetime import datetime, date

"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] and sve_karte[karta]["datum_prodaje"].date() == dan]
    return izvestaj

"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:

    izvesaj = [sve_karte[karta] for karta in sve_karte if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].date() == dan]
    return izvesaj

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    izvestaj = [sve_karte[karta] for karta in sve_karte if sve_karte[karta]["datum_prodaje"] and sve_karte[karta]["datum_prodaje"].date() == dan and sve_karte[karta]["prodavac"] == prodavac]
    return izvestaj

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] and sve_karte[karta]["datum_prodaje"].date() == dan:
            ukupan_broj += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return (ukupan_broj, ukupna_cena)

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:
    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].date() == dan or svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"] == dan: #!!!! treba da se ispravi na date
            ukupan_broj += 1
            ukupna_cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return (ukupan_broj, ukupna_cena)

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date,
    prodavac: str
) -> tuple:

    ukupan_broj = 0
    ukupna_cena = 0

    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"] and sve_karte[karta]["datum_prodaje"].date() == dan and sve_karte[karta]["prodavac"] == prodavac:
            ukupan_broj += 1
            ukupna_cena += svi_letovi[konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
    return (ukupan_broj, ukupna_cena)

"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    izvestaj  = {}

    for karta in sve_karte:
        if "prodavac" in sve_karte[karta] and sve_karte[karta]["prodavac"]:
            prodavac = sve_karte[karta]["prodavac"]["korisnicko_ime"]
        else:
            continue
        if prodavac not in izvestaj:
            izvestaj[prodavac] = {"ukupno_karata": 0, "ukupno_cena": 0}
        if prodavac in izvestaj and ((sve_karte[karta]["datum_prodaje"]-datetime.now()).days <= 30):
            izvestaj[prodavac]["ukupno_karata"] += 1
            izvestaj[prodavac]["ukupno_cena"] += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return izvestaj