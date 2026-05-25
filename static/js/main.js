const avionDataEl = document.getElementById("avionData");
const avionInfo = avionDataEl ? JSON.parse(avionDataEl.textContent) : null;

const avion = document.getElementById("avion");
const forma = document.getElementById("formaZaRezervaciju");
const izabranoSediste = document.getElementById("izabranoSediste");
const avionskaKarta = document.getElementById("karta");
const btnPrikazi = document.getElementById("prikaziRezervacije");
const listaRezervacija = document.getElementById("listaRezervacija");
const resetBtn = document.getElementById("reset");

let trenutnoSediste = null;
let rezervacije = [];

function kreirajSedista(broj) {
  if (!avion) return;

  avion.innerHTML = "";

  for (let i = 1; i <= broj; i++) {
    const sediste = document.createElement("div");
    const sedisteId = "A" + String(i).padStart(2, "0");

    sediste.classList.add("sediste");
    sediste.textContent = sedisteId;
    sediste.dataset.sediste = sedisteId;

    avion.appendChild(sediste);
  }
}

function ucitajRezervacijeNaSedista() {
  document.querySelectorAll(".sediste").forEach(sediste => {
    sediste.classList.remove("rezervisano", "selektovano");
    sediste.title = "";

    const sedisteId = sediste.dataset.sediste;
    const pronadjeno = rezervacije.find(r => r.sediste === sedisteId);

    if (pronadjeno) {
      sediste.classList.add("rezervisano");

      if (pronadjeno.moje) {
        sediste.title = `Moja rezervacija\nIme: ${pronadjeno.ime} ${pronadjeno.prezime}\nPasoš: ${pronadjeno.pasos}`;
      } else {
        sediste.title = `Rezervisano\nIme: ${pronadjeno.ime} ${pronadjeno.prezime}\nPasoš: ${pronadjeno.pasos}`;
      }
    }
  });
}

function biranjeSedista() {
  document.querySelectorAll(".sediste").forEach(sediste => {
    sediste.addEventListener("click", () => {
      if (avionskaKarta) {
        avionskaKarta.style.display = "none";
      }

      if (sediste.classList.contains("rezervisano")) return;

      document.querySelectorAll(".sediste").forEach(s => {
        s.classList.remove("selektovano");
      });

      sediste.classList.add("selektovano");

      trenutnoSediste = sediste.dataset.sediste;

      if (izabranoSediste) {
        izabranoSediste.textContent = trenutnoSediste;
      }

      if (forma) {
        forma.style.display = "block";
      }
    });
  });
}

async function ucitajRezervacije() {
  try {
    const response = await fetch(`/api/let/${letId}/rezervacije`);
    const data = await response.json();

    if (!response.ok) {
      alert(data.greska || "Greška pri učitavanju rezervacija.");
      return;
    }

    rezervacije = data.rezervacije || [];

    const info = document.getElementById("slobodnaMestaInfo");
    if (info) {
      info.textContent = `Trenutno slobodnih mesta: ${data.broj_slobodnih_mesta}`;
    }

    ucitajRezervacijeNaSedista();

    if (listaRezervacija && listaRezervacija.style.display === "block") {
      prikaziListuRezervacija();
    }
  } catch (error) {
    console.error("Greška:", error);
    alert("Došlo je do greške pri komunikaciji sa serverom.");
  }
}

function prikaziListuRezervacija() {
  if (!listaRezervacija || !avionInfo) return;

  if (rezervacije.length === 0) {
    listaRezervacija.innerHTML = "<p>Nema rezervacija za ovaj let.</p>";
    return;
  }

  let html = `
    <h3>Lista rezervacija – ${avionInfo.naziv}</h3>
    <ul>
  `;

  rezervacije.forEach(r => {
    html += `
      <li>
        <strong>Sedište:</strong> ${r.sediste} |
        <strong>Ime:</strong> ${r.ime} ${r.prezime} |
        <strong>Pasoš:</strong> ${r.pasos}
        ${r.moje ? ' <em>(moja rezervacija)</em>' : ''}
      </li>
    `;
  });

  html += "</ul>";
  listaRezervacija.innerHTML = html;
}

if (btnPrikazi) {
  btnPrikazi.addEventListener("click", () => {
    if (listaRezervacija.style.display === "none" || listaRezervacija.style.display === "") {
      prikaziListuRezervacija();
      listaRezervacija.style.display = "block";
      btnPrikazi.textContent = "Sakrij rezervacije";
    } else {
      listaRezervacija.style.display = "none";
      btnPrikazi.textContent = "Prikaži rezervacije";
    }
  });
}

if (forma) {
  forma.addEventListener("submit", async function (e) {
    e.preventDefault();

    const ime = document.getElementById("ime").value.trim();
    const prezime = document.getElementById("prezime").value.trim();
    const pasos = document.getElementById("pasos").value.trim();

    if (!ime || !prezime || !pasos || !trenutnoSediste) {
      alert("Popunite sva polja!");
      return;
    }

    try {
      const response = await fetch(`/api/let/${letId}/rezervacije`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          sediste: trenutnoSediste,
          ime: ime,
          prezime: prezime,
          pasos: pasos
        })
      });

      const rezultat = await response.json();

      if (!response.ok) {
        alert(rezultat.greska || "Došlo je do greške.");
        return;
      }

      const rezervacija = {
        sediste: trenutnoSediste,
        ime: ime,
        prezime: prezime,
        pasos: pasos
      };

      prikaziKartu(rezervacija);

      forma.reset();
      forma.style.display = "none";

      document.querySelectorAll(".sediste").forEach(s => {
        s.classList.remove("selektovano");
      });

      trenutnoSediste = null;

      await ucitajRezervacije();
    } catch (error) {
      console.error("Greška:", error);
      alert("Došlo je do greške pri slanju rezervacije.");
    }
  });
}

function prikaziKartu(r) {
  if (!avionskaKarta || !avionInfo) return;

  avionskaKarta.style.display = "block";
  avionskaKarta.innerHTML = `
    <h2>Avionska karta</h2>
    <p id="avionKarta"><strong>Avion:</strong> ${avionInfo.naziv}</p>
    <p id="imeKarta"><strong>Ime:</strong> ${r.ime} ${r.prezime}</p>
    <p id="sedisteKarta"><strong>Sedište:</strong> ${r.sediste}</p>
    <p id="pasosKarta"><strong>Broj pasoša:</strong> ${r.pasos}</p>
    <img src="${STIKER_URL}" alt="avion">
  `;
}

if (resetBtn) {
  resetBtn.addEventListener("click", async () => {
    const potvrda = confirm("Da li ste sigurni da želite da obrišete sve rezervacije za ovaj let?");
    if (!potvrda) return;

    try {
      const response = await fetch(`/api/let/${letId}/rezervacije/reset`, {
        method: "POST"
      });

      const rezultat = await response.json();

      if (!response.ok) {
        alert(rezultat.greska || "Greška pri brisanju rezervacija.");
        return;
      }

      rezervacije = [];
      trenutnoSediste = null;

      if (avionskaKarta) {
        avionskaKarta.style.display = "none";
      }

      if (forma) {
        forma.style.display = "none";
      }

      document.querySelectorAll(".sediste").forEach(s => {
        s.classList.remove("selektovano", "rezervisano");
        s.title = "";
      });

      await ucitajRezervacije();
      alert(rezultat.poruka || "Rezervacije su uspešno resetovane.");
    } catch (error) {
      console.error("Greška:", error);
      alert("Došlo je do greške pri resetovanju rezervacija.");
    }
  });
}

if (avionInfo && avionInfo.broj_sedista) {
  kreirajSedista(avionInfo.broj_sedista);
  biranjeSedista();
  ucitajRezervacije();
}