# TCX-tidsforskyvning

Noen ganger viser treningsklokker feil tidspunkt for start av aktivitet – for eksempel etter tomt batteri uten synkronisering. Da lagres økta med feil starttid og vises feil i tjenester som Strava. Dette er en enkel løsning for å justere starttid i TCX-filer.


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
    python tcx-starttime-editor.py

4. **Velg TCX-fil**

   Du skal få opp en filvelger. En ny fil genereres automatisk i samme mappe, med _newtime lagt til filnavnet.

