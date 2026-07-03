import json
from pathlib import Path

import pandas as pd
import streamlit as st

from models.drivers import DRIVERS

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


def create_driver_stats(data):
    stats = {
        driver: {
            "Jezdec": driver,
            "Tým": team,
            "Starty": 0,
            "Body": 0,
            "Body závod": 0,
            "Body sprint": 0,
            "Bonusové body": 0,
            "Výhry": 0,
            "Pódia": 0,
            "TOP 10": 0,
            "Nejrychlejší kola": 0,
            "Driver of the Day": 0,
            "Nejvíce předjetí": 0,
            "Nejčistší jezdec": 0
        }
        for driver, team in DRIVERS.items()
    }

    for race in data.get("races", []):
        bonuses = race.get("bonuses", {})

        for result in race.get("results", []):
            driver = result["Jezdec"]
            position = result["Pozice"]

            total_points = result.get("Body", 0)
            race_points = result.get("Body závod", total_points)
            sprint_points = result.get("Body sprint", 0)
            bonus_points = result.get("Bonusy", 0)

            stats[driver]["Starty"] += 1
            stats[driver]["Body"] += total_points
            stats[driver]["Body závod"] += race_points
            stats[driver]["Body sprint"] += sprint_points
            stats[driver]["Bonusové body"] += bonus_points

            if position == 1:
                stats[driver]["Výhry"] += 1

            if position <= 3:
                stats[driver]["Pódia"] += 1

            if position <= 10:
                stats[driver]["TOP 10"] += 1

        fastest_lap = bonuses.get("fastest_lap", "")
        driver_of_day = bonuses.get("driver_of_day", "")
        most_overtakes = bonuses.get("most_overtakes", "")
        cleanest_driver = bonuses.get("cleanest_driver", "")

        if fastest_lap in stats:
            stats[fastest_lap]["Nejrychlejší kola"] += 1

        if driver_of_day in stats:
            stats[driver_of_day]["Driver of the Day"] += 1

        if most_overtakes in stats:
            stats[most_overtakes]["Nejvíce předjetí"] += 1

        if cleanest_driver in stats:
            stats[cleanest_driver]["Nejčistší jezdec"] += 1

    table = pd.DataFrame(stats.values())

    table = table.sort_values(
        by=["Body", "Výhry", "Pódia", "TOP 10"],
        ascending=False
    )

    table.insert(0, "Pořadí", range(1, len(table) + 1))

    return table


st.title("📊 Statistiky")

data = load_data()
races_done = len(data.get("races", []))

if races_done == 0:
    st.info("Zatím není uložený žádný závod.")
    st.stop()

stats_table = create_driver_stats(data)

st.subheader("Souhrn sezóny")

col1, col2, col3, col4 = st.columns(4)

leader = stats_table.iloc[0]
most_wins = stats_table.sort_values(by="Výhry", ascending=False).iloc[0]
most_podiums = stats_table.sort_values(by="Pódia", ascending=False).iloc[0]
most_bonus = stats_table.sort_values(by="Bonusové body", ascending=False).iloc[0]

with col1:
    st.metric("Lídr šampionátu", leader["Jezdec"], f"{leader['Body']} bodů")

with col2:
    st.metric("Nejvíce výher", most_wins["Jezdec"], f"{most_wins['Výhry']} výher")

with col3:
    st.metric("Nejvíce pódií", most_podiums["Jezdec"], f"{most_podiums['Pódia']} pódií")

with col4:
    st.metric("Nejvíce bonusů", most_bonus["Jezdec"], f"{most_bonus['Bonusové body']} bodů")

st.divider()

st.subheader("Kompletní statistiky jezdců")

st.dataframe(
    stats_table,
    use_container_width="stretch",
    hide_index=True
)

st.divider()

st.subheader("TOP žebříčky")

col1, col2 = st.columns(2)

with col1:
    st.write("🏆 **Nejvíce výher**")
    st.dataframe(
        stats_table[["Jezdec", "Tým", "Výhry", "Pódia", "Body"]]
        .sort_values(by=["Výhry", "Pódia", "Body"], ascending=False)
        .head(10),
        use_container_width="stretch",
        hide_index=True
    )

    st.write("⚡ **Nejvíce sprintových bodů**")
    st.dataframe(
        stats_table[["Jezdec", "Tým", "Body sprint", "Body"]]
        .sort_values(by=["Body sprint", "Body"], ascending=False)
        .head(10),
        use_container_width="stretch",
        hide_index=True
    )

with col2:
    st.write("⭐ **Nejvíce bonusových bodů**")
    st.dataframe(
        stats_table[["Jezdec", "Tým", "Bonusové body", "Body"]]
        .sort_values(by=["Bonusové body", "Body"], ascending=False)
        .head(10),
        use_container_width="stretch",
        hide_index=True
    )

    st.write("🎯 **Nejvíce TOP 10 umístění**")
    st.dataframe(
        stats_table[["Jezdec", "Tým", "TOP 10", "Body"]]
        .sort_values(by=["TOP 10", "Body"], ascending=False)
        .head(10),
        use_container_width="stretch",
        hide_index=True
    )