import json
from pathlib import Path

import pandas as pd
import streamlit as st
import altair as alt

from models.drivers import DRIVERS

DRIVER_COLORS = {
    # Red Bull
    "Verstappen": "#62A8FF",
    "Hadjar": "#8DC2FF",

    # Ferrari
    "Hamilton": "#B60017",
    "Leclerc": "#FF1E2D",

    # McLaren
    "Piastri": "#FF8C1A",
    "Norris": "#FF6A00",

    # Mercedes
    "Russell": "#00D2BE",
    "Antonelli": "#00A894",

    # Aston Martin
    "Alonso": "#00B894",
    "Cpt. Franz Hermann": "#00E0A8",

    # Alpine
    "Colapinto": "#FF3DFF",
    "Gasly": "#FF66CC",

    # Haas
    "Bearman": "#BFC4C9",
    "Ocon": "#555C63",

    # Williams
    "Sainz": "#1746D6",
    "Albon": "#203C9F",

    # Audi
    "Luky ladič ^^": "#FF8A8A",
    "Bortoleto": "#D95F5F",

    # Racing Bulls
    "Lawson": "#F2F2F2",
    "Lindblad": "#8C8C8C",

    # Cadillac
    "Perez": "#D9C900",
    "Marshall": "#FFF04A"
}

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

def calculate_driver_points_history(data):
    totals = {
        driver: 0
        for driver in DRIVERS.keys()
    }

    rows = []

    for race in data.get("races", []):
        for result in race.get("results", []):
            driver = result.get("Jezdec")
            points = result.get("Body", 0)

            if driver not in totals:
                totals[driver] = 0

            totals[driver] += points

        row = {
            "Závod": race.get("race", "")
        }

        for driver, points in totals.items():
            row[driver] = points

        rows.append(row)

    return pd.DataFrame(rows)

data = load_data()

driver_table = calculate_driver_standings(data)
constructor_table = calculate_constructor_standings(data)

races_done = len(data["races"])
total_races = 24

def render_centered_table(df):
    styled_html = (
        df.to_html(index=False, escape=False)
        .replace(
            "<table border=\"1\" class=\"dataframe\">",
            "<table class=\"custom-table\">"
        )
    )

    st.markdown(
        """
        <style>
        .custom-table {
            width: 85%;
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse;
            font-size: 17px;
        }

        .custom-table th {
            text-align: center !important;
            padding: 10px;
            background-color: #1f222b;
            border: 1px solid #333842;
        }

        .custom-table td {
            text-align: center !important;
            padding: 9px;
            border: 1px solid #333842;
        }

        .custom-table tr:nth-child(even) {
            background-color: rgba(255, 255, 255, 0.03);
        }

        .custom-table tr:nth-child(odd) {
            background-color: rgba(255, 255, 255, 0.01);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(styled_html, unsafe_allow_html=True)


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

    st.divider()

st.subheader("📈 Vývoj bodů jezdců")

points_history = calculate_driver_points_history(data)

if points_history.empty:
    st.info("Graf vývoje bodů se zobrazí po prvním uloženém závodě.")
else:
    chart_data = points_history.set_index("Závod")

    chart_long = points_history.melt(
    id_vars="Závod",
    var_name="Jezdec",
    value_name="Body"
)

race_order = points_history["Závod"].tolist()

chart = (
    alt.Chart(chart_long)
    .mark_line(
        point=alt.OverlayMarkDef(
            filled=True,
            size=80
        )
    )
    .encode(
        x=alt.X(
            "Závod:N",
            sort=race_order,
            title="Závod"
        ),
        y=alt.Y(
    "Body:Q",
    title="Body",
    scale=alt.Scale(
        domainMin=0,
        zero=True)
        ),
        color=alt.Color(
    "Jezdec:N",
    title="Jezdec",
    scale=alt.Scale(
        domain=list(DRIVER_COLORS.keys()),
        range=list(DRIVER_COLORS.values())
    ),
    legend=alt.Legend(
    orient="bottom",
    direction="horizontal",
    columns=22,
    labelLimit=0,
    symbolSize=120,
    labelFontSize=15,
    title="Jezdec",
    columnPadding=35,
    labelOffset=6
)
    ),
        tooltip=[
            "Závod:N",
            "Jezdec:N",
            "Body:Q"
        ]
    )
    .properties(
        height=450
    )
    .interactive(
    bind_x=True,
    bind_y=False)
    )

st.altair_chart(
    chart,
    width="stretch"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("👤 TOP 5 jezdců")

    top_drivers = driver_table.head(5)[
        [
            "Pořadí",
            "Jezdec",
            "Tým",
            "Body",
            "Výhry",
            "Pódia"
        ]
    ]

    render_centered_table(top_drivers)

with col2:
    st.header("🏭 TOP 5 konstruktérů")

    top_constructors = constructor_table.head(5)[
        [
            "Pořadí",
            "Tým",
            "Body",
            "Výhry",
            "Pódia"
        ]
    ]

    render_centered_table(top_constructors)

