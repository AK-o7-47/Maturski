const avion = document.getElementById("avion");
const forma = document.getElementById("formaZaRezervaciju");
const izabranoSediste = document.getElementById("izabranoSediste");
const avionskaKarta = document.getElementById("karta");
const btnPrikazi = document.getElementById("prikaziRezervacije");
const listaRezervacija = document.getElementById("listaRezervacija");

let trenutnoSediste = null;
let rezervacije = [];

function kreirajSedista(broj) {
  avion.innerHTML = "";

  for (let i = 1; i <= broj; i++) {
    let sediste = document.createElement("div");
    let sedisteId = "A" + String(i).padStart(2, "0");

    sediste.classList.add("sediste");
    sediste.textContent = sedisteId;
    sediste.dataset.sediste = sedisteId;

    avion.appendChild(sediste);
  }
}

function ucitajRezervacijeNaSedista() {
  document.querySelectorAll(".sediste").forEach(sediste => {
    let sedisteId = sediste.dataset.sediste;
    let pronadjeno = rezervacije.find(r => r.sediste === sedisteId);

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
      avionskaKarta.style.display = "none";

      if (sediste.classList.contains("rezervisano")) return;

      trenutnoSediste = sediste.dataset.sediste;
      izabranoSediste.textContent = trenutnoSediste;
      forma.style.display = "block";
    });
  });
}

async function ucitajRezervacije() {
  const response = await fetch(`/api/let/${letId}/rezervacije`);
  const data = await response.json();

  rezervacije = data.rezervacije || [];

  const info = document.getElementById("slobodnaMestaInfo");
  if (info) {
    info.textContent = `Trenutno slobodnih mesta: ${data.broj_slobodnih_mesta}`;
  }

  ucitajRezervacijeNaSedista();

  if (listaRezervacija.style.display === "block") {
    prikaziListuRezervacija();
  }
}

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

function prikaziListuRezervacija() {
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

forma.addEventListener("submit", async function (e) {
  e.preventDefault();

  let ime = document.getElementById("ime").value.trim();
  let prezime = document.getElementById("prezime").value.trim();
  let pasos = document.getElementById("pasos").value.trim();

  if (!ime || !prezime || !pasos || !trenutnoSediste) {
    alert("Popunite sva polja!");
    return;
  }

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
  trenutnoSediste = null;

  await ucitajRezervacije();
});

function prikaziKartu(r) {
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

const resetBtn = document.getElementById("reset");

if (resetBtn) {
  resetBtn.addEventListener("click", async () => {
    const potvrda = confirm("Da li ste sigurni da želite da obrišete sve rezervacije za ovaj let?");
    if (!potvrda) return;

    const response = await fetch(`/api/let/${letId}/rezervacije/reset`, {
      method: "POST"
    });

    const rezultat = await response.json();

    if (!response.ok) {
      alert(rezultat.greska || "Greška pri brisanju rezervacija.");
      return;
    }

    rezervacije = [];
    await ucitajRezervacije();
    avionskaKarta.style.display = "none";
    forma.style.display = "none";
  });
}

kreirajSedista(avionInfo.brojSedista);
biranjeSedista();
ucitajRezervacije();