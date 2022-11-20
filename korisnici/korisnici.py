import common.konstante
from common import konstante

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""

def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:


    # if email == None:
    #     email = ""
    # if pasos == None:
    #     pasos = ""
    # if drzavljanstvo == None:
    #     drzavljanstvo = ""
    # if telefon == None:
    #     telefon = ""
    # if pol == None:
    #     telefon = ""

    if not isinstance(svi_korisnici, dict):
        return "Los unos, svi_korisnici nije tipa dict"
    if not isinstance(azuriraj, bool):
        return "Los unos, azuriraj nije boolian"

    for parametar in [uloga, korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol]:
        if not isinstance(parametar, str) or parametar == "":
            return f"Los unos, {parametar} nije tipa string ili je prazan"
    if azuriraj and staro_korisnicko_ime == None:
        return f"Los unos, azuriraj: {azuriraj} i staro_korisnicko_ime: {staro_korisnicko_ime}"
    
    for kljuc in svi_korisnici:
        if kljuc == None:
            return "Los unos"
        for kljuc_mali in svi_korisnici[kljuc]:
            if kljuc_mali == None:
                return "Los unos"

    if uloga not in [konstante.ULOGA_ADMIN, konstante.ULOGA_KORISNIK, konstante.ULOGA_PRODAVAC]:
        return f"Los unos, uloga: {uloga} nije dobrog tipa {konstante.ULOGA_ADMIN} ili {konstante.ULOGA_KORISNIK} ili {konstante.ULOGA_PRODAVAC}"
    if not pasos.isdecimal() or len(pasos) != 9:
        return f"Los unos, pasos: {pasos} ne moze biti konvertovan u string ili nema 9 karaktera"
    if "@" not in email:
        return f"Los unos, email: {email} neam @"
    else:
        email_lista = list(email)
        broj_tacaka = 0
        broj_et = 0
        for char in email_lista[email_lista.index("@"):]:
            if char == ".":
                broj_tacaka += 1
            if char == "@":
                broj_et += 1 
        if broj_tacaka != 1 or broj_et != 1 or (email_lista[email_lista.index("@")+1]) == "." or email_lista[email_lista.index("@")] == 0:
            return f"Los unos, email: {email} nije odgovarajuceg oblika"
    if not telefon.isdecimal():
        return f"Los unos, telefon: {telefon} ne moze biti konvertovn u int"

    if azuriraj:
        if (staro_korisnicko_ime in svi_korisnici and korisnicko_ime not in svi_korisnici) or (staro_korisnicko_ime in svi_korisnici and korisnicko_ime in svi_korisnici and korisnicko_ime == staro_korisnicko_ime):
            svi_korisnici[staro_korisnicko_ime]["korisnicko_ime"] = korisnicko_ime
            svi_korisnici[staro_korisnicko_ime]["lozinka"] = lozinka
            svi_korisnici[staro_korisnicko_ime]["ime"] = ime
            svi_korisnici[staro_korisnicko_ime]["prezime"] = prezime
            svi_korisnici[staro_korisnicko_ime]["uloga"] = uloga
            svi_korisnici[staro_korisnicko_ime]["email"] = email
            svi_korisnici[staro_korisnicko_ime]["pasos"] = pasos
            svi_korisnici[staro_korisnicko_ime]["drzavljanstvo"] = drzavljanstvo
            svi_korisnici[staro_korisnicko_ime]["telefon"] = telefon
            svi_korisnici[staro_korisnicko_ime]["pol"] = pol

            svi_korisnici[korisnicko_ime] = svi_korisnici.pop(staro_korisnicko_ime)

            return svi_korisnici
        else:
            return f"Los unos, staro_korisnicko_ime: {staro_korisnicko_ime} se ne nalazi u svi korisnici: {svi_korisnici}"
        
    else:
        if korisnicko_ime not in svi_korisnici:
            svi_korisnici[korisnicko_ime] = {}
            svi_korisnici[korisnicko_ime]["korisnicko_ime"] = korisnicko_ime
            svi_korisnici[korisnicko_ime]["lozinka"] = lozinka
            svi_korisnici[korisnicko_ime]["ime"] = ime
            svi_korisnici[korisnicko_ime]["prezime"] = prezime
            svi_korisnici[korisnicko_ime]["uloga"] = uloga
            svi_korisnici[korisnicko_ime]["email"] = email
            svi_korisnici[korisnicko_ime]["pasos"] = pasos
            svi_korisnici[korisnicko_ime]["drzavljanstvo"] = drzavljanstvo
            svi_korisnici[korisnicko_ime]["telefon"] = telefon
            svi_korisnici[korisnicko_ime]["pol"] = pol
            return svi_korisnici
        else:
            return f"Los unos, korisnicko_ime: {korisnicko_ime} vec postoji u svi_korisnici: {svi_korisnici}"
   

"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    HEADERS_LISTA = ["korisnicko_ime","lozinka","ime","prezime","uloga","pasos","drzavljanstvo","telefon","email","pol"]
    with open(putanja, "w") as f:
        for key in svi_korisnici:
            korisnik_dict = svi_korisnici[key]
            linija_lista = []
            for parametar in HEADERS_LISTA:
                linija_lista.append(korisnik_dict[parametar])
            linija = separator.join(linija_lista)
            f.write(linija+"\n")

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    ucitani_korisnici = {}
    HEADERS_LISTA = ["korisnicko_ime","lozinka","ime","prezime","uloga","pasos","drzavljanstvo","telefon","email","pol"]
    with open(putanja, "r") as f:
        for korisnik in f:
            korisnik = korisnik.split(separator)
            korisnik[-1] = korisnik[-1][:-1]
            ucitani_korisnici[korisnik[HEADERS_LISTA.index("korisnicko_ime")]] = {}
            for parametar in HEADERS_LISTA:
                ucitani_korisnici[korisnik[HEADERS_LISTA.index("korisnicko_ime")]][parametar] = korisnik[HEADERS_LISTA.index(parametar)] 
    return ucitani_korisnici

"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    if korisnicko_ime in svi_korisnici and svi_korisnici[korisnicko_ime]["korisnicko_ime"] == korisnicko_ime and svi_korisnici[korisnicko_ime]["lozinka"] == lozinka:
        return svi_korisnici[korisnicko_ime]
    else:
        return f"Los unos, korisnicko_ime i lozinka: {korisnicko_ime} : {lozinka} se ne nalaze u svi korisnici: {svi_korisnici}"
