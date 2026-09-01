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


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


st.title("📜 Historie závodů")

data = load_data()
races = data.get("races", [])

if not races:
    st.info("Zatím není uložený žádný závod.")

else:
    st.subheader("Uložené závody")

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

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Číslo závodu",
            selected_race.get("race_number", "")
        )

    with col2:
        st.metric(
            "Sprint",
            "Ano" if selected_race.get("sprint", False) else "Ne"
        )

    with col3:
        if selected_race.get("sprint", False):
            st.metric(
                "Sprint na mokru",
                "Ano" if selected_race.get("sprint_wet", False) else "Ne"
            )
        else:
            st.metric("Sprint na mokru", "—")

    with col4:
        st.metric(
            "Závod na mokru",
            "Ano" if selected_race.get("race_wet", False) else "Ne"
        )

    with col5:
        st.metric(
            "Počet výsledků",
            len(selected_race.get("results", []))
        )

    st.divider()

    if selected_race.get("sprint_results"):
        st.subheader("⚡ Výsledky sprintu")

        sprint_results = pd.DataFrame(selected_race["sprint_results"])

        st.dataframe(
            sprint_results,
            use_container_width="stretch",
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
        use_container_width="stretch",
        hide_index=True
    )

    st.divider()

    st.subheader("🏁 Výsledky závodu")

    results = pd.DataFrame(selected_race.get("results", []))

    st.dataframe(
        results,
        use_container_width="stretch",
        hide_index=True
    )

    st.divider()

    st.subheader("Nebezpečná zóna")

    confirm_delete = st.checkbox(
        f"Chci smazat závod {selected_race['race']}"
    )

    if st.button("🗑️ Smazat vybraný závod"):
        if confirm_delete:
            data["races"].pop(selected_index)
            data["current_race"] = len(data["races"])
            save_data(data)

            st.success("Závod byl smazán. Obnov stránku.")
            st.rerun()
        else:
            st.error("Nejdřív potvrď zaškrtnutím checkboxu.")

    st.divider()

    st.subheader("Reset celé sezóny")

    confirm_reset = st.checkbox("Chci smazat všechny uložené závody")

    if st.button("🧹 Resetovat sezónu"):
        if confirm_reset:
            data["races"] = []
            data["current_race"] = 0
            save_data(data)

            st.success("Sezóna byla resetována.")
            st.rerun()
        else:
            st.error("Nejdřív potvrď reset zaškrtnutím checkboxu.")