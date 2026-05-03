from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "moja_tajna_lozinka_za_sesiju_123"
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = os.path.join(BASE_DIR, "aviokompanija.db")

AVIONI = [
    {"id": "a320", "naziv": "Airbus A320", "brojSedista": 180},
    {"id": "b737", "naziv": "Boeing 737", "brojSedista": 160},
    {"id": "atr72", "naziv": "ATR 72", "brojSedista": 70},
    {"id": "atr73", "naziv": "ATR 73", "brojSedista": 130}
]
KAPACITETI_AVIONA = {
    "a320": 180,
    "b737": 160,
    "atr72": 70,
    "atr73": 130
}

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_avion_by_id(avion_id):
    for avion in AVIONI:
        if avion["id"] == avion_id:
            return avion
    return None
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        ime = request.form["ime"].strip()
        prezime = request.form["prezime"].strip()
        email = request.form["email"].strip().lower()
        lozinka = request.form["lozinka"]

        if not ime or not prezime or not email or not lozinka:
            return render_template("signup.html", greska="Sva polja su obavezna.")

        hashed_lozinka = generate_password_hash(lozinka)

        conn = get_db_connection()
        postojeci = conn.execute("SELECT * FROM korisnici WHERE email = ?", (email,)).fetchone()

        if postojeci:
            conn.close()
            return render_template("signup.html", greska="Korisnik sa tim emailom već postoji.")

        conn.execute("""
            INSERT INTO korisnici (ime, prezime, email, lozinka, uloga)
            VALUES (?, ?, ?, ?, ?)
        """, (ime, prezime, email, hashed_lozinka, "korisnik"))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        lozinka = request.form["lozinka"]

        conn = get_db_connection()
        korisnik = conn.execute("SELECT * FROM korisnici WHERE email = ?", (email,)).fetchone()
        conn.close()

        if korisnik and check_password_hash(korisnik["lozinka"], lozinka):
            session["korisnik_id"] = korisnik["id"]
            session["ime"] = korisnik["ime"]
            session["prezime"] = korisnik["prezime"]
            session["email"] = korisnik["email"]
            session["uloga"] = korisnik["uloga"]

            return redirect(url_for("index2"))

        return render_template("login.html", greska="Pogrešan email ili lozinka.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index2"))
@app.context_processor
def inject_user():
    return {
        "ulogovan": "korisnik_id" in session,
        "session_ime": session.get("ime"),
        "session_prezime": session.get("prezime"),
        "session_uloga": session.get("uloga")
    }
@app.route("/")
def index2():
    conn = get_db_connection()
    aerodromi = conn.execute("SELECT * FROM aerodromi ORDER BY grad").fetchall()
    conn.close()
    return render_template("index2.html", aerodromi=aerodromi, rezultati=None)


@app.route("/pretraga")
def pretraga_letova():
    polaziste = request.args.get("polaziste", "").strip()
    odrediste = request.args.get("odrediste", "").strip()
    datum_od = request.args.get("datum_od", "").strip()
    datum_do = request.args.get("datum_do", "").strip()
    max_cena = request.args.get("max_cena", "").strip()

    query = """
        SELECT l.*,
               ap.grad AS polaziste_grad,
               ap.drzava AS polaziste_drzava,
               ap.iata_kod AS polaziste_kod,
               ao.grad AS odrediste_grad,
               ao.drzava AS odrediste_drzava,
               ao.iata_kod AS odrediste_kod
        FROM letovi l
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        WHERE 1=1
    """
    params = []

    if polaziste:
        query += " AND l.polaziste_id = ?"
        params.append(polaziste)

    if odrediste:
        query += " AND l.odrediste_id = ?"
        params.append(odrediste)

    if datum_od:
        query += " AND date(l.datum_polaska) >= date(?)"
        params.append(datum_od)

    if datum_do:
        query += " AND date(l.datum_polaska) <= date(?)"
        params.append(datum_do)

    if max_cena:
        query += " AND l.cena <= ?"
        params.append(max_cena)

    query += " ORDER BY l.datum_polaska ASC"

    conn = get_db_connection()
    rezultati = conn.execute(query, params).fetchall()
    aerodromi = conn.execute("SELECT * FROM aerodromi ORDER BY grad").fetchall()
    conn.close()

    return render_template("index2.html", aerodromi=aerodromi, rezultati=rezultati)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "korisnik_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "korisnik_id" not in session:
            return redirect(url_for("login"))
        if session.get("uloga") != "admin":
            return redirect(url_for("index2"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/let/<int:let_id>")
def let_detalji(let_id):
    conn = get_db_connection()
    let = conn.execute("""
        SELECT l.*,
               ap.naziv AS polaziste_naziv,
               ap.grad AS polaziste_grad,
               ap.drzava AS polaziste_drzava,
               ap.iata_kod AS polaziste_kod,
               ao.naziv AS odrediste_naziv,
               ao.grad AS odrediste_grad,
               ao.drzava AS odrediste_drzava,
               ao.iata_kod AS odrediste_kod
        FROM letovi l
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        WHERE l.id = ?
    """, (let_id,)).fetchone()
    conn.close()

    if let is None:
        return "Let nije pronađen.", 404

    avion = get_avion_by_id(let["tip_aviona"])
    return render_template("let_detalji.html", let=let, avion=avion)


@app.route("/let/<int:let_id>/rezervacija")
@login_required
def rezervacija_leta(let_id):
    conn = get_db_connection()
    let = conn.execute("""
        SELECT l.*,
               ap.grad AS polaziste_grad,
               ap.iata_kod AS polaziste_kod,
               ao.grad AS odrediste_grad,
               ao.iata_kod AS odrediste_kod
        FROM letovi l
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        WHERE l.id = ?
    """, (let_id,)).fetchone()
    conn.close()

    if let is None:
        return "Let nije pronađen.", 404

    avion = get_avion_by_id(let["tip_aviona"])
    if avion is None:
        return "Tip aviona za ovaj let nije pronađen.", 404

    korisnik = {
        "ime": session.get("ime", ""),
        "prezime": session.get("prezime", "")
    }

    return render_template("index.html", let=let, avion=avion, korisnik=korisnik)

@app.route("/api/let/<int:let_id>/rezervacije")
@login_required
def api_rezervacije(let_id):
    conn = get_db_connection()

    rezervacije = conn.execute("""
        SELECT r.id, r.korisnik_id, r.sediste, r.ime, r.prezime, r.pasos
        FROM rezervacije r
        WHERE r.let_id = ?
        ORDER BY r.sediste
    """, (let_id,)).fetchall()

    let = conn.execute("""
        SELECT broj_slobodnih_mesta
        FROM letovi
        WHERE id = ?
    """, (let_id,)).fetchone()

    conn.close()

    trenutni_korisnik_id = session.get("korisnik_id")

    rezervacije_lista = []
    for r in rezervacije:
        rezervacije_lista.append({
            "id": r["id"],
            "sediste": r["sediste"],
            "ime": r["ime"],
            "prezime": r["prezime"],
            "pasos": r["pasos"],
            "moje": r["korisnik_id"] == trenutni_korisnik_id
        })

    return jsonify({
        "rezervacije": rezervacije_lista,
        "broj_slobodnih_mesta": let["broj_slobodnih_mesta"] if let else 0
    })

@app.route("/api/let/<int:let_id>/rezervacije", methods=["POST"])
@login_required
def api_dodaj_rezervaciju(let_id):
    data = request.get_json()

    sediste = data.get("sediste", "").strip()
    ime = data.get("ime", "").strip()
    prezime = data.get("prezime", "").strip()
    pasos = data.get("pasos", "").strip()
    korisnik_id = session.get("korisnik_id")

    if not all([sediste, ime, prezime, pasos]):
        return jsonify({"greska": "Sva polja su obavezna."}), 400

    conn = get_db_connection()

    let = conn.execute("""
        SELECT id, broj_slobodnih_mesta
        FROM letovi
        WHERE id = ?
    """, (let_id,)).fetchone()

    if let is None:
        conn.close()
        return jsonify({"greska": "Let nije pronađen."}), 404

    if let["broj_slobodnih_mesta"] <= 0:
        conn.close()
        return jsonify({"greska": "Nema više slobodnih mesta na ovom letu."}), 400

    postojeca = conn.execute("""
        SELECT id FROM rezervacije
        WHERE let_id = ? AND sediste = ?
    """, (let_id, sediste)).fetchone()

    if postojeca:
        conn.close()
        return jsonify({"greska": "Ovo sedište je već rezervisano."}), 400

    conn.execute("""
        INSERT INTO rezervacije (korisnik_id, let_id, sediste, ime, prezime, pasos)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (korisnik_id, let_id, sediste, ime, prezime, pasos))

    conn.execute("""
        UPDATE letovi
        SET broj_slobodnih_mesta = broj_slobodnih_mesta - 1
        WHERE id = ?
    """, (let_id,))

    conn.commit()
    conn.close()

    return jsonify({"poruka": "Rezervacija uspešno sačuvana."})
@app.route("/api/let/<int:let_id>/rezervacije/reset", methods=["POST"])
@admin_required
def api_reset_rezervacija(let_id):
    conn = get_db_connection()

    let = conn.execute("""
        SELECT tip_aviona
        FROM letovi
        WHERE id = ?
    """, (let_id,)).fetchone()

    if let is None:
        conn.close()
        return jsonify({"greska": "Let nije pronađen."}), 404

    kapacitet = KAPACITETI_AVIONA.get(let["tip_aviona"], 0)

    conn.execute("DELETE FROM rezervacije WHERE let_id = ?", (let_id,))
    conn.execute("""
        UPDATE letovi
        SET broj_slobodnih_mesta = ?
        WHERE id = ?
    """, (kapacitet, let_id))

    conn.commit()
    conn.close()

    return jsonify({"poruka": "Rezervacije su obrisane i broj slobodnih mesta je resetovan."})

@app.route("/moje-rezervacije")
@login_required
def moje_rezervacije():
    korisnik_id = session.get("korisnik_id")

    conn = get_db_connection()
    rezervacije = conn.execute("""
        SELECT r.id, r.sediste, r.ime, r.prezime, r.pasos,
               l.broj_leta, l.aviokompanija, l.datum_polaska, l.cena,
               ap.grad AS polaziste_grad, ap.iata_kod AS polaziste_kod,
               ao.grad AS odrediste_grad, ao.iata_kod AS odrediste_kod
        FROM rezervacije r
        JOIN letovi l ON r.let_id = l.id
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        WHERE r.korisnik_id = ?
        ORDER BY l.datum_polaska ASC
    """, (korisnik_id,)).fetchall()
    conn.close()

    return render_template("moje_rezervacije.html", rezervacije=rezervacije)

@app.route("/rezervacija/otkazi/<int:rezervacija_id>")
@login_required
def otkazi_rezervaciju(rezervacija_id):
    korisnik_id = session.get("korisnik_id")

    conn = get_db_connection()

    rezervacija = conn.execute("""
        SELECT * FROM rezervacije
        WHERE id = ? AND korisnik_id = ?
    """, (rezervacija_id, korisnik_id)).fetchone()

    if rezervacija is None:
        conn.close()
        return redirect(url_for("moje_rezervacije"))

    conn.execute("DELETE FROM rezervacije WHERE id = ?", (rezervacija_id,))
    conn.execute("""
        UPDATE letovi
        SET broj_slobodnih_mesta = broj_slobodnih_mesta + 1
        WHERE id = ?
    """, (rezervacija["let_id"],))

    conn.commit()
    conn.close()

    return redirect(url_for("moje_rezervacije"))

@app.route("/sve-rezervacije")
@admin_required
def sve_rezervacije():
    broj_leta = request.args.get("broj_leta", "").strip()
    email = request.args.get("email", "").strip()
    putnik = request.args.get("putnik", "").strip()
    sediste = request.args.get("sediste", "").strip()

    query = """
        SELECT r.id, r.sediste, r.ime, r.prezime, r.pasos,
               k.ime AS korisnik_ime, k.prezime AS korisnik_prezime, k.email AS korisnik_email,
               l.id AS let_id, l.broj_leta, l.aviokompanija, l.datum_polaska, l.cena,
               ap.grad AS polaziste_grad, ap.iata_kod AS polaziste_kod,
               ao.grad AS odrediste_grad, ao.iata_kod AS odrediste_kod
        FROM rezervacije r
        JOIN korisnici k ON r.korisnik_id = k.id
        JOIN letovi l ON r.let_id = l.id
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        WHERE 1=1
    """
    params = []

    if broj_leta:
        query += " AND l.broj_leta LIKE ?"
        params.append(f"%{broj_leta}%")

    if email:
        query += " AND k.email LIKE ?"
        params.append(f"%{email}%")

    if putnik:
        query += " AND (r.ime LIKE ? OR r.prezime LIKE ?)"
        params.append(f"%{putnik}%")
        params.append(f"%{putnik}%")

    if sediste:
        query += " AND r.sediste LIKE ?"
        params.append(f"%{sediste}%")

    query += " ORDER BY l.datum_polaska ASC"

    conn = get_db_connection()
    rezervacije = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("sve_rezervacije.html", rezervacije=rezervacije)
@app.route("/admin/rezervacija/obrisi/<int:rezervacija_id>")
@admin_required
def admin_obrisi_rezervaciju(rezervacija_id):
    conn = get_db_connection()

    rezervacija = conn.execute("""
        SELECT * FROM rezervacije
        WHERE id = ?
    """, (rezervacija_id,)).fetchone()

    if rezervacija is None:
        conn.close()
        return redirect(url_for("sve_rezervacije"))

    conn.execute("DELETE FROM rezervacije WHERE id = ?", (rezervacija_id,))
    conn.execute("""
        UPDATE letovi
        SET broj_slobodnih_mesta = broj_slobodnih_mesta + 1
        WHERE id = ?
    """, (rezervacija["let_id"],))

    conn.commit()
    conn.close()

    return redirect(url_for("sve_rezervacije"))
# -------------------------
# CRUD AERODROMI
# -------------------------

@app.route("/aerodromi")
@admin_required
def lista_aerodroma():
    conn = get_db_connection()
    aerodromi = conn.execute("SELECT * FROM aerodromi ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("aerodromi.html", aerodromi=aerodromi)


@app.route("/aerodromi/dodaj", methods=["GET", "POST"])
@admin_required
def dodaj_aerodrom():
    if request.method == "POST":
        naziv = request.form["naziv"].strip()
        grad = request.form["grad"].strip()
        drzava = request.form["drzava"].strip()
        iata_kod = request.form["iata_kod"].strip().upper()

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO aerodromi (naziv, grad, drzava, iata_kod)
            VALUES (?, ?, ?, ?)
        """, (naziv, grad, drzava, iata_kod))
        conn.commit()
        conn.close()

        return redirect(url_for("lista_aerodroma"))

    return render_template("aerodrom_forma.html", aerodrom=None)


@app.route("/aerodromi/izmeni/<int:id>", methods=["GET", "POST"])
@admin_required
def izmeni_aerodrom(id):
    conn = get_db_connection()
    aerodrom = conn.execute("SELECT * FROM aerodromi WHERE id = ?", (id,)).fetchone()

    if aerodrom is None:
        conn.close()
        return "Aerodrom nije pronađen.", 404

    if request.method == "POST":
        naziv = request.form["naziv"].strip()
        grad = request.form["grad"].strip()
        drzava = request.form["drzava"].strip()
        iata_kod = request.form["iata_kod"].strip().upper()

        conn.execute("""
            UPDATE aerodromi
            SET naziv = ?, grad = ?, drzava = ?, iata_kod = ?
            WHERE id = ?
        """, (naziv, grad, drzava, iata_kod, id))
        conn.commit()
        conn.close()

        return redirect(url_for("lista_aerodroma"))

    conn.close()
    return render_template("aerodrom_forma.html", aerodrom=aerodrom)


@app.route("/aerodromi/obrisi/<int:id>")
@admin_required
def obrisi_aerodrom(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM aerodromi WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("lista_aerodroma"))


# -------------------------
# CRUD LETOVI
# -------------------------

@app.route("/letovi")
@admin_required
def lista_letova():
    conn = get_db_connection()
    letovi = conn.execute("""
        SELECT l.*,
               ap.grad AS polaziste_grad,
               ap.iata_kod AS polaziste_kod,
               ao.grad AS odrediste_grad,
               ao.iata_kod AS odrediste_kod
        FROM letovi l
        JOIN aerodromi ap ON l.polaziste_id = ap.id
        JOIN aerodromi ao ON l.odrediste_id = ao.id
        ORDER BY l.id DESC
    """).fetchall()
    conn.close()

    return render_template("letovi.html", letovi=letovi, avioni=AVIONI)


@app.route("/letovi/dodaj", methods=["GET", "POST"])
@admin_required
def dodaj_let():
    conn = get_db_connection()
    aerodromi = conn.execute("SELECT * FROM aerodromi ORDER BY grad").fetchall()

    if request.method == "POST":
        broj_leta = request.form["broj_leta"].strip().upper()
        aviokompanija = request.form["aviokompanija"].strip()
        tip_aviona = request.form["tip_aviona"]
        polaziste_id = request.form["polaziste_id"]
        odrediste_id = request.form["odrediste_id"]
        datum_polaska = request.form["datum_polaska"]
        datum_dolaska = request.form["datum_dolaska"]
        cena = request.form["cena"]
        broj_slobodnih_mesta = request.form["broj_slobodnih_mesta"]

        conn.execute("""
            INSERT INTO letovi (
                broj_leta, aviokompanija, tip_aviona, polaziste_id, odrediste_id,
                datum_polaska, datum_dolaska, cena, broj_slobodnih_mesta
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            broj_leta,
            aviokompanija,
            tip_aviona,
            polaziste_id,
            odrediste_id,
            datum_polaska,
            datum_dolaska,
            cena,
            broj_slobodnih_mesta
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("lista_letova"))

    conn.close()
    return render_template("let_forma.html", let=None, aerodromi=aerodromi, avioni=AVIONI)


@app.route("/letovi/izmeni/<int:id>", methods=["GET", "POST"])
@admin_required
def izmeni_let(id):
    conn = get_db_connection()
    let = conn.execute("SELECT * FROM letovi WHERE id = ?", (id,)).fetchone()
    aerodromi = conn.execute("SELECT * FROM aerodromi ORDER BY grad").fetchall()

    if let is None:
        conn.close()
        return "Let nije pronađen.", 404

    if request.method == "POST":
        broj_leta = request.form["broj_leta"].strip().upper()
        aviokompanija = request.form["aviokompanija"].strip()
        tip_aviona = request.form["tip_aviona"]
        polaziste_id = request.form["polaziste_id"]
        odrediste_id = request.form["odrediste_id"]
        datum_polaska = request.form["datum_polaska"]
        datum_dolaska = request.form["datum_dolaska"]
        cena = request.form["cena"]
        broj_slobodnih_mesta = request.form["broj_slobodnih_mesta"]

        conn.execute("""
            UPDATE letovi
            SET broj_leta = ?, aviokompanija = ?, tip_aviona = ?, polaziste_id = ?, odrediste_id = ?,
                datum_polaska = ?, datum_dolaska = ?, cena = ?, broj_slobodnih_mesta = ?
            WHERE id = ?
        """, (
            broj_leta,
            aviokompanija,
            tip_aviona,
            polaziste_id,
            odrediste_id,
            datum_polaska,
            datum_dolaska,
            cena,
            broj_slobodnih_mesta,
            id
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("lista_letova"))

    conn.close()
    return render_template("let_forma.html", let=let, aerodromi=aerodromi, avioni=AVIONI)


@app.route("/letovi/obrisi/<int:id>")
@admin_required
def obrisi_let(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM letovi WHERE id = ?", (id,))
    conn.execute("DELETE FROM rezervacije WHERE let_id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("lista_letova"))


if __name__ == "__main__":
    app.run(debug=True)