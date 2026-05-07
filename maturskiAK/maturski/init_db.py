import sqlite3

conn = sqlite3.connect("aviokompanija.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS korisnici (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    prezime TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    lozinka TEXT NOT NULL,
    uloga TEXT NOT NULL CHECK(uloga IN ('admin', 'korisnik'))
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS aerodromi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naziv TEXT NOT NULL,
    grad TEXT NOT NULL,
    drzava TEXT NOT NULL,
    iata_kod TEXT NOT NULL UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS letovi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    broj_leta TEXT NOT NULL UNIQUE,
    aviokompanija TEXT NOT NULL,
    tip_aviona TEXT NOT NULL,
    polaziste_id INTEGER NOT NULL,
    odrediste_id INTEGER NOT NULL,
    datum_polaska TEXT NOT NULL,
    datum_dolaska TEXT NOT NULL,
    cena REAL NOT NULL,
    broj_slobodnih_mesta INTEGER NOT NULL,
    FOREIGN KEY (polaziste_id) REFERENCES aerodromi(id),
    FOREIGN KEY (odrediste_id) REFERENCES aerodromi(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS rezervacije (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    korisnik_id INTEGER NOT NULL,
    let_id INTEGER NOT NULL,
    sediste TEXT NOT NULL,
    ime TEXT NOT NULL,
    prezime TEXT NOT NULL,
    pasos TEXT NOT NULL,
    FOREIGN KEY (korisnik_id) REFERENCES korisnici(id),
    FOREIGN KEY (let_id) REFERENCES letovi(id)
)
""")

conn.commit()
conn.close()

print("Baza uspešno kreirana.")