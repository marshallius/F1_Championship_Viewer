import json
from io import BytesIO
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


def calculate_driver_standings(data):
    standings = {
        driver: {
            "Jezdec": driver,
            "Tým": team,
            "Body": 0,
            "Body závod": 0,
            "Body sprint": 0,
            "Bonusové body": 0,
            "Výhry": 0,
            "Pódia": 0,
            "TOP 10": 0
        }
        for driver, team in DRIVERS.items()
    }

    for race in data.get("races", []):
        for result in race.get("results", []):
            driver = result["Jezdec"]
            position = result["Pozice"]

            total_points = result.get("Body", 0)
            race_points = result.get("Body závod", total_points)
            sprint_points = result.get("Body sprint", 0)
            bonus_points = result.get("Bonusy", 0)

            standings[driver]["Body"] += total_points
            standings[driver]["Body závod"] += race_points
            standings[driver]["Body sprint"] += sprint_points
            standings[driver]["Bonusové body"] += bonus_points

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
            "Bonusové body": 0,
            "Výhry": 0,
            "Pódia": 0
        }
        for team in teams
    }

    for race in data.get("races", []):
        for result in race.get("results", []):
            team = result["Tým"]
            position = result["Pozice"]

            total_points = result.get("Body", 0)
            race_points = result.get("Body závod", total_points)
            sprint_points = result.get("Body sprint", 0)
            bonus_points = result.get("Bonusy", 0)

            standings[team]["Body"] += total_points
            standings[team]["Body závod"] += race_points
            standings[team]["Body sprint"] += sprint_points
            standings[team]["Bonusové body"] += bonus_points

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


def create_race_results_table(data):
    rows = []

    for race in data.get("races", []):
        race_name = race.get("race", "")
        race_number = race.get("race_number", "")
        sprint = race.get("sprint", False)

        for result in race.get("results", []):
            rows.append({
                "Číslo závodu": race_number,
                "Závod": race_name,
                "Sprint víkend": "Ano" if sprint else "Ne",
                "Pozice": result.get("Pozice", ""),
                "Jezdec": result.get("Jezdec", ""),
                "Tým": result.get("Tým", ""),
                "Body závod": result.get("Body závod", result.get("Body", 0)),
                "Body sprint": result.get("Body sprint", 0),
                "Bonusy": result.get("Bonusy", 0),
                "Body celkem": result.get("Body", 0)
            })

    return pd.DataFrame(rows)


def create_sprint_results_table(data):
    rows = []

    for race in data.get("races", []):
        race_name = race.get("race", "")
        race_number = race.get("race_number", "")

        for result in race.get("sprint_results", []):
            rows.append({
                "Číslo závodu": race_number,
                "Závod": race_name,
                "Sprint pozice": result.get("Sprint pozice", ""),
                "Jezdec": result.get("Jezdec", ""),
                "Tým": result.get("Tým", ""),
                "Body": result.get("Body", 0)
            })

    return pd.DataFrame(rows)


def create_bonus_table(data):
    rows = []

    bonus_names = {
        "fastest_lap": "Nejrychlejší kolo",
        "driver_of_day": "Driver of the Day",
        "most_overtakes": "Nejvíce předjetí",
        "cleanest_driver": "Nejčistší jezdec"
    }

    for race in data.get("races", []):
        bonuses = race.get("bonuses", {})

        for key, label in bonus_names.items():
            rows.append({
                "Závod": race.get("race", ""),
                "Bonus": label,
                "Jezdec": bonuses.get(key, "")
            })

    return pd.DataFrame(rows)


def create_excel_file(data):
    output = BytesIO()

    driver_standings = calculate_driver_standings(data)
    constructor_standings = calculate_constructor_standings(data)
    race_results = create_race_results_table(data)
    sprint_results = create_sprint_results_table(data)
    bonus_table = create_bonus_table(data)

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        driver_standings.to_excel(writer, sheet_name="Jezdci", index=False)
        constructor_standings.to_excel(writer, sheet_name="Konstruktéři", index=False)
        race_results.to_excel(writer, sheet_name="Výsledky závodů", index=False)
        sprint_results.to_excel(writer, sheet_name="Sprinty", index=False)
        bonus_table.to_excel(writer, sheet_name="Bonusy", index=False)

    output.seek(0)

    return output


st.title("📤 Export sezóny")

data = load_data()
races_done = len(data.get("races", []))

if races_done == 0:
    st.info("Zatím není uložený žádný závod, není co exportovat.")
    st.stop()

st.write(f"Odjeté závody: **{races_done}**")

excel_file = create_excel_file(data)

st.download_button(
    label="📥 Stáhnout Excel",
    data=excel_file,
    file_name=f"F1_Championship_Manager_{data['season']}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

json_text = json.dumps(data, indent=4, ensure_ascii=False)

st.download_button(
    label="📦 Stáhnout zálohu JSON",
    data=json_text,
    file_name=f"F1_Championship_Manager_{data['season']}_backup.json",
    mime="application/json"
)