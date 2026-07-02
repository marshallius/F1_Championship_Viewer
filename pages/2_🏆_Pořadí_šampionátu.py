import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Pořadí šampionátu",
    page_icon="🏆",
    layout="wide"
)

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


def calculate_driver_standings(data):
    standings = {
        driver: {
            "Jezdec": driver,
            "Tým": team,
            "Body": 0,
            "Body závod": 0,
            "Body sprint": 0,
            "Bonusy": 0,
            "Výhry": 0,
            "Pódia": 0,
            "TOP 10": 0
        }
        for driver, team in DRIVERS.items()
    }

    for race in data.get("races", []):
        for result in race.get("results", []):
            driver = result.get("Jezdec", "")

            if driver not in standings:
                continue

            position = result.get("Pozice", 0)

            total_points = result.get("Body", 0)
            race_points = result.get("Body závod", total_points)
            sprint_points = result.get("Body sprint", 0)
            bonus_points = result.get("Bonusy", 0)

            standings[driver]["Body"] += total_points
            standings[driver]["Body závod"] += race_points
            standings[driver]["Body sprint"] += sprint_points
            standings[driver]["Bonusy"] += bonus_points

            if position == 1:
                standings[driver]["Výhry"] += 1

            if position <= 3:
                standings[driver]["Pódia"] += 1

            if position <= 10:
                standings[driver]["TOP 10"] += 1

    table = pd.DataFrame(standings.values())

    table = table.sort_values(
        by=["Body", "Výhry", "Pódia", "TOP 10"],
        ascending=False
    )

    table.insert(0, "Pořadí", range(1, len(table) + 1))

    return table


def calculate_constructor_standings(data):
    teams = sorted(set(DRIVERS.values()))

    standings = {
        team: {
            "Tým": team,
            "Body": 0,
            "Body závod": 0,
            "Body sprint": 0,
            "Bonusy": 0,
            "Výhry": 0,
            "Pódia": 0,
            "TOP 10": 0
        }
        for team in teams
    }

    for race in data.get("races", []):
        for result in race.get("results", []):
            team = result.get("Tým", "")

            if team not in standings:
                continue

            position = result.get("Pozice", 0)

            total_points = result.get("Body", 0)
            race_points = result.get("Body závod", total_points)
            sprint_points = result.get("Body sprint", 0)
            bonus_points = result.get("Bonusy", 0)

            standings[team]["Body"] += total_points
            standings[team]["Body závod"] += race_points
            standings[team]["Body sprint"] += sprint_points
            standings[team]["Bonusy"] += bonus_points

            if position == 1:
                standings[team]["Výhry"] += 1

            if position <= 3:
                standings[team]["Pódia"] += 1

            if position <= 10:
                standings[team]["TOP 10"] += 1

    table = pd.DataFrame(standings.values())

    table = table.sort_values(
        by=["Body", "Výhry", "Pódia", "TOP 10"],
        ascending=False
    )

    table.insert(0, "Pořadí", range(1, len(table) + 1))

    return table


st.title("🏆 Pořadí šampionátu")

data = load_data()
races_done = len(data.get("races", []))

driver_table = calculate_driver_standings(data)
constructor_table = calculate_constructor_standings(data)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Odjeté závody", races_done)

with col2:
    leader_driver = driver_table.iloc[0]
    st.metric(
        "Lídr jezdců",
        leader_driver["Jezdec"],
        f"{leader_driver['Body']} bodů"
    )

with col3:
    leader_constructor = constructor_table.iloc[0]
    st.metric(
        "Lídr konstruktérů",
        leader_constructor["Tým"],
        f"{leader_constructor['Body']} bodů"
    )

st.divider()

left, right = st.columns([2, 1])

st.subheader("👤 Pořadí jezdců")

st.dataframe(
    driver_table,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🏭 Pořadí konstruktérů")

st.dataframe(
    constructor_table,
    use_container_width=True,
    hide_index=True
)
