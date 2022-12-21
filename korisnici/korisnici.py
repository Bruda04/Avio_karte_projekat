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


    if not isinstance(svi_korisnici, dict):    #provera da li je svi_korisnici dictionary
        raise Exception("Los unos, svi_korisnici nije tipa dict")
    if not isinstance(azuriraj, bool):    #provera da li je azuriraj boolian
        raise Exception("Los unos, azuriraj nije boolian")

    for parametar in [uloga, korisnicko_ime, lozinka, ime, prezime, email, telefon]:
        if not isinstance(parametar, str) or parametar == "" or parametar == None:    #provera da li su parametri stringovi ili prazni stringovi
            raise Exception(f"Los unos, {parametar} nije tipa string ili je prazan")
    if azuriraj and (staro_korisnicko_ime == ""  or staro_korisnicko_ime == None or not isinstance(staro_korisnicko_ime, str)):    #provera da li je prosledjeno staro_korisnicko_ime kada je postavljeno azuriraj na True
        raise Exception(f"Los unos, azuriraj: {azuriraj} i staro_korisnicko_ime: {staro_korisnicko_ime}")
    
    for kljuc in svi_korisnici:    #provera internih gresaka kljuceva
        if kljuc == None:
            raise Exception("Los unos")
        for kljuc_mali in svi_korisnici[kljuc]:
            if kljuc_mali == None:
                raise Exception("Los unos")

    if uloga not in [konstante.ULOGA_ADMIN, konstante.ULOGA_KORISNIK, konstante.ULOGA_PRODAVAC]:    #provera da li je prosledjena validna uloga
        raise Exception(f"Los unos, uloga: {uloga} nije dobrog tipa {konstante.ULOGA_ADMIN} ili {konstante.ULOGA_KORISNIK} ili {konstante.ULOGA_PRODAVAC}")
    if pasos != "" and pasos != None and (not pasos.isdecimal() or len(pasos) != 9):     #provera da li je pasos u validnom obliku
        raise Exception(f"Los unos, pasos: {pasos} ne moze biti konvertovan u string ili nema 9 karaktera")
    if "@" not in email:    #provera da li email sadrzi @
        raise Exception(f"Los unos, email: {email} neam @")
    else:    #provera da li email sadrzi samo jedan poddomen
        email_lista = list(email)
        broj_tacaka = 0
        broj_et = 0
        for char in email_lista[email_lista.index("@"):]:
            if char == ".":
                broj_tacaka += 1
            if char == "@":
                broj_et += 1 
        if broj_tacaka != 1 or broj_et != 1 or (email_lista[email_lista.index("@")+1]) == "." or email_lista[email_lista.index("@")] == 0:
            raise Exception(f"Los unos, email: {email} nije odgovarajuceg oblika")
    if not telefon.isdecimal():    #provera da li je telefon u validnom obliku
        raise Exception(f"Los unos, telefon: {telefon} ne moze biti konvertovn u int")

    if azuriraj:    #azuriranje svih parametara korisnika
        if (staro_korisnicko_ime in svi_korisnici and korisnicko_ime not in svi_korisnici) or (staro_korisnicko_ime in svi_korisnici and korisnicko_ime in svi_korisnici and korisnicko_ime == staro_korisnicko_ime):    #provera da li je novo korisnicko ime vec zauzeto
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

            svi_korisnici[korisnicko_ime] = svi_korisnici.pop(staro_korisnicko_ime)    #menja kljuc i zadrzava vrednosti na koje je ukazivao prosli kljuc
            
            return svi_korisnici
        else:
            raise Exception(f"Los unos, staro_korisnicko_ime: {staro_korisnicko_ime} se ne nalazi u svi korisnici: {svi_korisnici}")
        
    else:    #dodavanje novog korisnika u dictionary svi_korisnici
        if korisnicko_ime not in svi_korisnici:    #provera da li je korisnicko ime vec zauzeto
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
            raise Exception(f"Los unos, korisnicko_ime: {korisnicko_ime} vec postoji u svi_korisnici: {svi_korisnici}")


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    HEADERS_LISTA = konstante.PARAMETRI_KORISNIKA
    with open(putanja, "w") as f:
        for key in svi_korisnici:    #prolazak kroz sve korisnike
            korisnik_dict = svi_korisnici[key]    #dictionary trenutnog korisnika
            linija_lista = []    #lista koja ce sadrzati parametre
            for parametar in HEADERS_LISTA:
                linija_lista.append(korisnik_dict[parametar])    #dodavanje parametara trenutnog korisnika u listu
            linija = separator.join(linija_lista)    #konverovanje liste u liniju(korisnika) u csv formatu
            f.write(linija+"\n")

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    ucitani_korisnici = {}    
    HEADERS_LISTA = konstante.PARAMETRI_KORISNIKA
    with open(putanja, "r") as f:
        for korisnik in f:    #prolazak kroz sve linije(korisnike)
            korisnik = korisnik.split(separator)    #korisnik je ovde lista sa vrednostima parametara korisnika
            korisnik[-1] = korisnik[-1][:-1]    #uklanjanje \n sa kraja linije
            ucitani_korisnici[korisnik[HEADERS_LISTA.index("korisnicko_ime")]] = {}    #postavljanje kljuca na dictionary korisnika i pravljenje samog dictionary-a za korisnika 
            for parametar in HEADERS_LISTA:
                ucitani_korisnici[korisnik[HEADERS_LISTA.index("korisnicko_ime")]][parametar] = korisnik[HEADERS_LISTA.index(parametar)]    #postavljanje parametara za svakog korisnika u njegovom dictionary-u
    return ucitani_korisnici

ulogovan = None

"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    if korisnicko_ime in svi_korisnici and svi_korisnici[korisnicko_ime]["korisnicko_ime"] == korisnicko_ime and svi_korisnici[korisnicko_ime]["lozinka"] == lozinka:    #provera da li korisnik postoji i da li su njegovi uneti parametri validni
        global ulogovan
        ulogovan = svi_korisnici[korisnicko_ime]
        return svi_korisnici[korisnicko_ime]
    else:
        raise Exception(f"Los unos, korisnicko_ime i lozinka: {korisnicko_ime} : {lozinka} se ne nalaze u svi korisnici: {svi_korisnici}")



"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    global ulogovan
    ulogovan = None


"""
Funkcija koja vraca recnik korisnika koji je ulogovan
"""
def ko_je_ulogovan() -> dict:
    global ulogovan
    return ulogovan

