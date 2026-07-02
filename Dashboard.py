import json
from pathlib import Path

import pandas as pd
import streamlit as st

from models.drivers import DRIVERS

DATA_FILE = Path("data/championship.json")

st.set_page_config(
    page_title="F1 Championship Manager",
    page_icon="🏁",
    layout="wide"
)


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
            "Výhry": 0,
            "Pódia": 0
        }
        for driver, team in DRIVERS.items()
    }

    for race in data["races"]:
        for result in race["results"]:
            driver = result["Jezdec"]
            position = result["Pozice"]
            points = result["Body"]

            standings[driver]["Body"] += points

            if position == 1:
                standings[driver]["Výhry"] += 1

            if position <= 3:
                standings[driver]["Pódia"] += 1

    table = pd.DataFrame(standings.values())

    table = table.sort_values(
        by=["Body", "Výhry", "Pódia"],
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
            "Výhry": 0,
            "Pódia": 0
        }
        for team in teams
    }

    for race in data["races"]:
        for result in race["results"]:
            team = result["Tým"]
            position = result["Pozice"]
            points = result["Body"]

            standings[team]["Body"] += points

            if position == 1:
                standings[team]["Výhry"] += 1

            if position <= 3:
                standings[team]["Pódia"] += 1

    table = pd.DataFrame(standings.values())

    table = table.sort_values(
        by=["Body", "Výhry", "Pódia"],
        ascending=False
    )

    table.insert(0, "Pořadí", range(1, len(table) + 1))

    return table


data = load_data()

driver_table = calculate_driver_standings(data)
constructor_table = calculate_constructor_standings(data)

races_done = len(data["races"])
total_races = 24

st.title("🏁 F1 Championship Manager")
st.subheader(f"Sezóna {data['season']}")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Odjeté závody", f"{races_done} / {total_races}")

with col2:
    leader_driver = driver_table.iloc[0]
    st.metric(
        "Lídr jezdců",
        leader_driver["Jezdec"],
        f"{leader_driver['Body']} bodů"
    )

with col3:
    leader_team = constructor_table.iloc[0]
    st.metric(
        "Lídr konstruktérů",
        leader_team["Tým"],
        f"{leader_team['Body']} bodů"
    )

with col4:
    st.metric("Počet jezdců", len(DRIVERS))

st.divider()

if races_done == 0:
    st.info("Zatím není uložený žádný závod.")
else:
    last_race = data["races"][-1]

    st.header("🏆 Poslední závod")
    st.subheader(last_race["race"])

    last_results = pd.DataFrame(last_race["results"])

    podium = last_results.head(3)

    col1, col2, col3 = st.columns(3)

    with col1:
        winner = podium.iloc[0]
        st.metric("🥇 Vítěz", winner["Jezdec"], f"{winner['Body']} bodů")

    with col2:
        second = podium.iloc[1]
        st.metric("🥈 Druhé místo", second["Jezdec"], f"{second['Body']} bodů")

    with col3:
        third = podium.iloc[2]
        st.metric("🥉 Třetí místo", third["Jezdec"], f"{third['Body']} bodů")

    st.dataframe(
        last_results,
        use_container_width=True,
        hide_index=True
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("👤 TOP 5 jezdců")
    st.dataframe(
        driver_table.head(5),
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.header("🏭 TOP 5 konstruktérů")
    st.dataframe(
        constructor_table.head(5),
        use_container_width=True,
        hide_index=True
    )