Pokretanje aplikacije
Otvoriti Command Prompt (Windows).
Uneti komandu:
cd path
(putanja do foldera gde se nalazi aplikacija, npr. C:\Users\Aleksa\Desktop\maturski)
Pokrenuti aplikaciju komandom:
python app.py
U Command Prompt-u će se pojaviti poruka tipa:
Running on http://127.0.0.1:5000
Taj link uneti u internet pretraživač i aplikacija će se otvoriti.
Aplikacija se zatvara pritiskom na:
CTRL + C
u Command Prompt-u.

Funkcionalnost stranice
Guest korisnik
Na početnoj strani nalazi se Pretraga letova.
Kao GUEST korisnik možemo:
	Pretraživati letove
	Pregledati dostupne letove
Za rezervaciju karata potrebno je imati nalog.
Registracija i prijava
Klikom na dugme Login vrši se prijava.
Ako korisnik nema nalog, klikom na Signup otvara se forma za registraciju.
Unose se sledeći podaci:
	Ime
	Prezime
	Email
	Lozinka
Klikom na dugme Registruj se nalog se kreira.
Rezervacija letova
Nakon uspešne prijave:
Omogućena je rezervacija karata
Pojavljuje se dugme Moje rezervacije
Moguće je pregledati sve rezervisane letove
Pretraga letova
Ako se klikne na dugme Pretraži bez unosa podataka, prikazuju se svi dostupni letovi.
Letovi se mogu filtrirati po:
	Polazištu
	Odredištu
	Datumu (od – do)
	Maksimalnoj ceni (EUR)
Detalji leta
Klikom na Detalji leta prikazuju se:
Informacije o letu
Informacije o avionu
Klikom na Rezerviši sedište otvara se prikaz sedišta u avionu:
	Crvena sedišta – zauzeta
	Ostala sedišta – slobodna
Korisnik bira sedište, unosi broj pasoša i klikom na Rezerviši uspešno rezerviše kartu.
Odjava
Klikom na dugme Logout korisnik se odjavljuje sa naloga.