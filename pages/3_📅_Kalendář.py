import json
from pathlib import Path

import pandas as pd
import streamlit as st

from models.calendar import RACES

DATA_FILE = Path("data/championship.json")


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return {
        "season": 2026,
        "current_race": 0,
        "races": []
    }


st.title("📅 Kalendář sezóny")

data = load_data()
saved_races = data.get("races", [])

completed_race_names = [
    race["race"]
    for race in saved_races
]

calendar_rows = []

for race in RACES:
    race_name = race["name"]

    if race_name in completed_race_names:
        status = "✅ Odjeto"
    else:
        status = "⏳ Čeká"

    calendar_rows.append({
        "Číslo": race["number"],
        "Závod": race_name,
        "Sprint": "Ano" if race["sprint"] else "Ne",
        "Stav": status
    })

calendar_table = pd.DataFrame(calendar_rows)

st.dataframe(
    calendar_table,
    use_container_width="stretch",
    hide_index=True
)

st.divider()

completed = len(completed_race_names)
total = len(RACES)

st.metric("Průběh sezóny", f"{completed} / {total}")

if completed < total:
    next_race = RACES[completed]
    st.info(f"Další závod: {next_race['name']}")
else:
    st.success("Sezóna je dokončená.")