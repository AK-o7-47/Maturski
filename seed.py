import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("aviokompanija.db")
cur = conn.cursor()

# -------------------------
# ADMIN KORISNIK
# -------------------------
admin_email = "admin@avio.rs"
admin_lozinka = generate_password_hash("admin123")

try:
    cur.execute("""
    INSERT INTO korisnici (ime, prezime, email, lozinka, uloga)
    VALUES (?, ?, ?, ?, ?)
    """, ("Admin", "Admin", admin_email, admin_lozinka, "admin"))
except sqlite3.IntegrityError:
    pass

# -------------------------
# AERODROMI
# -------------------------
aerodromi = [
    ("Nikola Tesla", "Beograd", "Srbija", "BEG"),
    ("Franjo Tuđman", "Zagreb", "Hrvatska", "ZAG"),
    ("Schwechat", "Beč", "Austrija", "VIE"),
    ("Charles de Gaulle", "Pariz", "Francuska", "CDG"),
    ("Heathrow", "London", "Velika Britanija", "LHR"),
    ("Haneda", "Tokio", "Japan", "HND"),
    ("Narita", "Tokio", "Japan", "NRT"),
    ("Bali Ngurah Rai", "Denpasar", "Indonezija", "DPS"),
    ("Ibiza Airport", "Ibiza", "Španija", "IBZ"),
    ("Beijing Capital", "Peking", "Kina", "PEK")
]

for a in aerodromi:
    try:
        cur.execute("""
        INSERT INTO aerodromi (naziv, grad, drzava, iata_kod)
        VALUES (?, ?, ?, ?)
        """, a)
    except sqlite3.IntegrityError:
        pass

# -------------------------
# AVIONI - NOVO
# -------------------------
avioni = [
    ("a320", "Airbus A320", 180),
    ("b737", "Boeing 737", 160),
    ("atr72", "ATR 72", 70),
    ("atr73", "ATR 73", 130)
]

for av in avioni:
    try:
        cur.execute("""
        INSERT INTO avioni (id, naziv, broj_sedista)
        VALUES (?, ?, ?)
        """, av)
    except sqlite3.IntegrityError:
        pass

# -------------------------
# LETOVI
# -------------------------
letovi = [
    ("JU101", "Air Serbia", "a320", 1, 3, "2026-06-10 08:00", "2026-06-10 09:20", 120, 180),
    ("JU102", "Air Serbia", "a320", 3, 1, "2026-06-11 14:00", "2026-06-11 15:20", 115, 180),
    ("LH200", "Lufthansa", "b737", 1, 4, "2026-06-15 06:30", "2026-06-15 09:10", 220, 160),
    ("AF333", "Air France", "atr72", 4, 5, "2026-06-16 12:00", "2026-06-16 13:10", 95, 70),
    ("BA777", "British Airways", "b737", 5, 6, "2026-07-01 10:00", "2026-07-02 08:00", 780, 160),
    ("NH555", "ANA", "a320", 6, 8, "2026-07-10 09:30", "2026-07-10 18:40", 640, 180),
    ("QF101", "Qantas", "a320", 8, 6, "2026-07-20 19:00", "2026-07-21 06:30", 670, 180),
    ("IB202", "Iberia", "atr73", 3, 9, "2026-08-02 11:15", "2026-08-02 14:00", 180, 130),
    ("CA888", "Air China", "b737", 10, 6, "2026-08-05 13:00", "2026-08-05 23:00", 520, 160),
    ("TK404", "Turkish Airlines", "a320", 1, 10, "2026-09-01 07:00", "2026-09-01 15:30", 410, 180)
]

for l in letovi:
    try:
        cur.execute("""
        INSERT INTO letovi (
            broj_leta, aviokompanija, tip_aviona, polaziste_id, odrediste_id,
            datum_polaska, datum_dolaska, cena, broj_slobodnih_mesta
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, l)
    except sqlite3.IntegrityError:
        pass

conn.commit()
conn.close()

print("Podaci uspešno uneti.")