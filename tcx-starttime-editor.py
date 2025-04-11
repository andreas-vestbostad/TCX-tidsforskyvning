import tkinter as tk
from tkinter import filedialog
from xml.etree import ElementTree as ET
from datetime import datetime
from pathlib import Path
import logging

# === Ny starttid i ISO 8601-format ===
desired_start_time_str = "2025-04-11T12:34:56.789Z"

# === Sett opp logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Registrer XML-navnerom brukt i TCX-filer ===
ET.register_namespace('', "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
ET.register_namespace('ext', "http://www.garmin.com/xmlschemas/ActivityExtension/v2")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

def parse_time(t):
    """Parser ISO 8601-tid, med eller uten millisekunder"""
    try:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")

def format_time(dt):
    """Formatterer datetime til ISO 8601 med millisekunder og 'Z'"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def log_error(message, element=None):
    """Logg feil"""
    if element is not None:
        logging.error(f"{message} (Element: {ET.tostring(element, encoding='unicode')})")
    else:
        logging.error(message)

def validate_input(element, name):
    """Validerer om et element har gyldig data"""
    if element is None or not element.text.strip():
        log_error(f"Ugyldig {name} - ingen data funnet", element)
        return False
    return True

def main():
    # === Vis filvelger for å velge .tcx-fil ===
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Velg TCX-fil", filetypes=[("TCX files", "*.tcx")])
    if not file_path:
        logging.error("Ingen fil valgt.")
        return

    desired_start = parse_time(desired_start_time_str)

    # === Les XML fra valgt fil ===
    try:
        tree = ET.parse(file_path)
    except Exception as e:
        log_error(f"Feil ved lesing av fil: {e}")
        return

    root_el = tree.getroot()
    ns_uri = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
    ns = {'ns': ns_uri}

    # === Finn alle <Time>-elementer ===
    all_times = root_el.findall(".//ns:Time", ns)
    if not all_times:
        logging.error("Fant ingen <Time>-elementer.")
        return

    # === Beregn tidsforskjell fra første <Time> til ønsket starttid ===
    try:
        original_start = parse_time(all_times[0].text)
    except Exception as e:
        log_error(f"Feil ved parsing av starttid: {e}", all_times[0])
        return

    delta = desired_start - original_start
    logging.info(f"Forskyver alle tidspunkter med: {delta}")

    # === Oppdater alle <Time>-elementer ===
    for t in all_times:
        if validate_input(t, "<Time>"):
            try:
                t_dt = parse_time(t.text)
                t.text = format_time(t_dt + delta)
            except Exception as e:
                log_error(f"Feil ved oppdatering av <Time>: {e}", t)

    # === Oppdater <Id>-element (aktivitetens navn) ===
    id_tag = root_el.find(".//ns:Id", ns)
    if id_tag is not None and validate_input(id_tag, "<Id>"):
        try:
            id_dt = parse_time(id_tag.text)
            id_tag.text = format_time(id_dt + delta)
        except Exception as e:
            log_error(f"Feil ved oppdatering av <Id>: {e}", id_tag)

    # === Oppdater StartTime-attributt i <Lap>-element(er) ===
    lap_tags = root_el.findall(".//ns:Lap", ns)
    for lap in lap_tags:
        start_time_str = lap.attrib.get("StartTime")
        if start_time_str:
            try:
                lap_dt = parse_time(start_time_str)
                lap.attrib["StartTime"] = format_time(lap_dt + delta)
            except Exception as e:
                log_error(f"Feil ved oppdatering av <Lap StartTime>: {e}", lap)

    # === Lagre ny fil med "_newtime" lagt til filnavnet ===
    output_file = Path(file_path).with_name(Path(file_path).stem + "_newtime.tcx")
    try:
        with open(output_file, 'wb') as out_file:
            tree.write(out_file, encoding="utf-8", xml_declaration=True)
        logging.info(f"Ny fil lagret som: {output_file}")
    except Exception as e:
        log_error(f"Feil ved lagring av ny fil: {e}")

if __name__ == "__main__":
    main()