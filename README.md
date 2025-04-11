# ⏱️ TCX-tidsforskyvning

⚡ **Enkel løsning for å justere starttid i TCX-filer fra treningsklokker**

## 📌 Hva er dette?

Noen ganger viser treningsklokka feil tidspunkt – for eksempel etter tomt batteri uten synkronisering. Da lagres økta med feil starttid og vises feil i tjenester som Strava.

Mens det finnes gode verktøy for FIT-filer, er det få som fungerer bra for TCX-formatet. Denne applikasjonen lar deg enkelt justere starttidspunktet i en .tcx-fil slik at hele aktiviteten forskyves korrekt i tid.

## 🛠️ Funksjoner

- 📂 Leser TCX-filer eksportert fra treningsapper
- ⏱️ Lar deg spesifisere ønsket starttid i ISO 8601-format (`YYYY-MM-DDTHH:MM:SS.sssZ`)
- 🔄 Oppdaterer:
  - Alle `<Time>`-elementer
  - `<Id>`-elementet (aktivitetens ID/navn)
  - `StartTime`-attributter i `<Lap>`-tagger
- 💾 Skriver en ny TCX-fil med oppdatert tidspunkt (originalfilen beholdes uendret)

## 🧑‍💻 Bruk

1. **Installer nødvendige biblioteker:**

   Programmet bruker kun Python sitt standardbibliotek. Skulle noe mangle kan du installere det manuelt:

   ```bash
   pip install tk
   pip install pathlib

2. **Angi ønsket starttid:**

   Endre følgende linje:
   ```python
    desired_start_time_str = "2025-04-11T12:34:56.789Z"

3. **Kjør skriptet:**
   ```bash
    python tcx_time_shifter.py

4. **Velg TCX-filen du ønsker å korrigere**

5. **Ferdig!**

    En ny fil genereres automatisk i samme mappe, med _newtime lagt til filnavnet. Eksempel:
    originalfil.tcx  →  originalfil_newtime.tcx
