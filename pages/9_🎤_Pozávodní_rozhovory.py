from pathlib import Path
from urllib.parse import quote

import streamlit as st

from models.calendar import RACES


COMMENTS_DIR = Path("comments")
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/marshalius/F1_Championship_Viewer/main"


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

    if " " in name:
        first_part, rest = name.split(" ", 1)

        if first_part.isdigit():
            return rest

    return name


def get_image_url(image_path):
    relative_path = image_path.as_posix()
    encoded_path = quote(relative_path, safe="/")
    return f"{GITHUB_RAW_BASE}/{encoded_path}"


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
            margin-bottom: 0.5rem;
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
        image_name = clean_image_name(image_path)

        with columns[index]:
            st.image(
                str(image_path),
                width="stretch"
            )

            st.markdown(
                f'<div class="interview-name">{image_name}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="interview-note">Pozávodní rozhovor</div>',
                unsafe_allow_html=True
            )

            st.link_button(
                "🔍 Otevřít ve velkém",
                get_image_url(image_path),
                width="stretch"
            )

    if len(images) > 3:
        st.caption(f"V tomto závodě je nahráno {len(images)} obrázků, zobrazují se první 3.")