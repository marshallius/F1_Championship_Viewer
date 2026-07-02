import json
from pathlib import Path

import pandas as pd
import streamlit as st

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


st.title("📜 Historie závodů")

data = load_data()
races = data.get("races", [])

if not races:
    st.info("Zatím není uložený žádný závod.")
else:
    race_names = [
        f"{index + 1}. {race['race']}"
        for index, race in enumerate(races)
    ]

    selected_race_label = st.selectbox(
        "Vyber závod",
        race_names
    )

    selected_index = race_names.index(selected_race_label)
    selected_race = races[selected_index]

    st.divider()

    st.header(selected_race["race"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Číslo závodu", selected_race.get("race_number", ""))

    with col2:
        st.metric("Sprint", "Ano" if selected_race.get("sprint", False) else "Ne")

    with col3:
        st.metric("Počet výsledků", len(selected_race.get("results", [])))

    st.divider()

    if selected_race.get("sprint_results"):
        st.subheader("⚡ Výsledky sprintu")

        sprint_results = pd.DataFrame(selected_race["sprint_results"])

        st.dataframe(
            sprint_results,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

    st.subheader("⭐ Bonusové body")

    bonuses = selected_race.get("bonuses", {})

    bonus_table = pd.DataFrame([
        {
            "Bonus": "Nejrychlejší kolo",
            "Jezdec": bonuses.get("fastest_lap", "")
        },
        {
            "Bonus": "Driver of the Day",
            "Jezdec": bonuses.get("driver_of_day", "")
        },
        {
            "Bonus": "Nejvíce předjetí",
            "Jezdec": bonuses.get("most_overtakes", "")
        },
        {
            "Bonus": "Nejčistší jezdec",
            "Jezdec": bonuses.get("cleanest_driver", "")
        }
    ])

    st.dataframe(
        bonus_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🏁 Výsledky závodu")

    results = pd.DataFrame(selected_race["results"])

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )