from pathlib import Path

import streamlit as st

from models.calendar import RACES


COMMENTS_DIR = Path("comments")
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]


def get_race_images(race_name):
    race_dir = COMMENTS_DIR / race_name

    if not race_dir.exists():
        return []

    images = [
        file
        for file in race_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    return sorted(images, key=lambda file: file.name.lower())


def clean_image_name(image_path):
    name = image_path.stem

    # Když bude soubor pojmenovaný třeba "01 Marshall",
    # odstraní se jen úvodní číslo.
    if " " in name:
        first_part, rest = name.split(" ", 1)

        if first_part.isdigit():
            return rest

    return name


def set_magazine_style():
    st.markdown(
        """
        <style>
        .magazine-title {
            font-size: 42px;
            font-weight: 900;
            margin-bottom: 0.2rem;
        }

        .magazine-subtitle {
            font-size: 17px;
            color: #b8c0cc;
            margin-bottom: 2rem;
        }

        .race-title {
            font-size: 32px;
            font-weight: 850;
            margin-top: 2.3rem;
            margin-bottom: 1.1rem;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.18);
        }

        .interview-card {
            background: rgba(18, 21, 30, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 12px;
            box-shadow: 0 10px 26px rgba(0,0,0,0.35);
            margin-bottom: 1.2rem;
        }

        .interview-name {
            text-align: center;
            font-size: 18px;
            font-weight: 800;
            margin-top: 0.7rem;
            color: #ffffff;
        }

        .interview-note {
            text-align: center;
            font-size: 13px;
            color: #aeb6c2;
            margin-top: 0.2rem;
        }

        .empty-race {
            color: #8f98a8;
            font-size: 15px;
            margin-bottom: 1rem;
        }

        img {
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


set_magazine_style()

st.markdown(
    '<div class="magazine-title">🎤 Pozávodní rozhovory</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="magazine-subtitle">Magazín pozávodních komentářů jezdců podle jednotlivých Grand Prix.</div>',
    unsafe_allow_html=True
)

for race in RACES:
    race_name = race["name"]
    images = get_race_images(race_name)

    st.markdown(
        f'<div class="race-title">{race["number"]}. {race_name}</div>',
        unsafe_allow_html=True
    )

    if not images:
        st.markdown(
            '<div class="empty-race">Zatím nejsou nahrané žádné pozávodní rozhovory.</div>',
            unsafe_allow_html=True
        )
        continue

    columns = st.columns(3)

    for index, image_path in enumerate(images[:3]):
        with columns[index]:
            st.markdown('<div class="interview-card">', unsafe_allow_html=True)

            st.image(
                str(image_path),
                width="stretch"
            )

            st.markdown(
                f"""
                <div class="interview-name">{clean_image_name(image_path)}</div>
                <div class="interview-note">Pozávodní rozhovor</div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

    if len(images) > 3:
        st.caption(f"V tomto závodě je nahráno {len(images)} obrázků, zobrazují se první 3.")