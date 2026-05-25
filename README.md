# ✈️ Sistem za rezervaciju avionskih karata

Web aplikacija za pretragu, pregled i rezervaciju avionskih letova sa funkcionalnostima za goste i registrovane korisnike.

---

## 📑 Sadržaj
- [🚀 Pokretanje aplikacije](#-pokretanje-aplikacije)
- [🌐 Funkcionalnosti](#-funkcionalnosti)
  - [👤 Gost korisnik](#-gost-korisnik)
  - [🔐 Registracija i prijava](#-registracija-i-prijava)
  - [🎫 Rezervacija letova](#-rezervacija-letova)
  - [🔍 Pretraga letova](#-pretraga-letova)
  - [✈️ Detalji leta i rezervacija sedišta](#-detalji-leta-i-rezervacija-sedišta)
  - [🚪 Odjava](#-odjava)
- [🛠️ Tehnologije](#-tehnologije)
- [📝 Napomene](#-napomene)

---

## 🚀 Pokretanje aplikacije

1. Otvorite **Command Prompt** (Windows) ili bilo koji terminal.
2. Navigirajte do foldera gde se nalazi aplikacija:

```bash
cd putanja/do/foldera
# Primer:
cd C:\Users\Aleksa\Desktop\maturski
```

3. Pokrenite aplikaciju:

```bash
python app.py
```

4. U terminalu će se pojaviti poruka:

```bash
Running on http://127.0.0.1:5000
```

Otvorite navedeni link u internet pretraživaču kako biste pristupili aplikaciji.

5. Za zaustavljanje aplikacije pritisnite:

```bash
CTRL + C
```

---

## 🌐 Funkcionalnosti

### 👤 Gost korisnik

Na početnoj strani nalazi se **Pretraga letova**.

Kao gost korisnik moguće je:

- Pretraživati letove  
- Pregledati dostupne letove  

> Za rezervaciju karata potrebno je imati nalog.

---

### 🔐 Registracija i prijava

Klikom na dugme **Login** vrši se prijava.

Ako korisnik nema nalog, klikom na **Signup** otvara se forma za registraciju.

Unose se sledeći podaci:

- Ime  
- Prezime  
- Email  
- Lozinka  

Klikom na dugme **Registruj se** nalog se uspešno kreira.

---

### 🎫 Rezervacija letova

Nakon uspešne prijave omogućeno je:

- Rezervisanje karata  
- Dugme **Moje rezervacije**  
- Pregled svih rezervisanih letova  

---

### 🔍 Pretraga letova

Ako se klikne na dugme **Pretraži** bez unosa podataka, prikazuju se svi dostupni letovi.

Letovi se mogu filtrirati po:

- Polazištu  
- Odredištu  
- Datumu (od – do)  
- Maksimalnoj ceni (EUR)  

---

### ✈️ Detalji leta i rezervacija sedišta

Klikom na **Detalji leta** prikazuju se:

- Informacije o letu  
- Informacije o avionu  

Klikom na **Rezerviši sedište** otvara se prikaz sedišta u avionu:

- 🔴 Crvena sedišta – zauzeta  
- ⚪ Ostala sedišta – slobodna  

Korisnik bira sedište, unosi broj pasoša i klikom na **Rezerviši** uspešno rezerviše kartu.

---

### 🚪 Odjava

Klikom na dugme **Logout** korisnik se odjavljuje sa naloga.

---

## 🛠️ Tehnologije

- Python  
- Flask  
- HTML  
- CSS  
- JavaScript  
- SQLite / MySQL  

---

## 📝 Napomene

- Potrebno je imati instaliran **Python 3.x**.  
- Preporučuje se korišćenje virtuelnog okruženja.  
- Aplikacija je namenjena za edukativne svrhe.  
