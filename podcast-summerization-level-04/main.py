from api_communication import *
import streamlit as st
import json

st.title("Welcome to Podcast summeries")
# saving this id to show in the website as a header
episode_id = st.sidebar.text_input("Please give us the episode-id")
run_btn = st.sidebar.button(
    "Get Summery",
    on_click=save_transcript,
    args=(episode_id, True)
)


def cala_time(start_ms):
    sec = int((start_ms / 1000) % 60)
    min = int((start_ms/(1000 * 60)) % 60)
    hr = int((start_ms/(1000 * 60 * 60)) % 24)
    if (hr > 0):
        time = f"{hr:02d}:{min:02d}:{sec:02d}"
    elif (min > 0):
        time = f"{min:02d}:{sec:02d}"
    else:
        time = f"{sec:02d}"

    return time


if run_btn:
    filename = episode_id + "_chapters.json"
    with open(filename, "r") as f:
        data = json.load(f)

        chapters = data["chapters"]
        thumbnail = data["episode_thumbnail"]
        episode_title = data["episode_title"]
        podcast_title = data["podcast_title"]

    st.header(f"{podcast_title} - {episode_title}")
    st.image(thumbnail)

    for chp in chapters:
        with st.expander(chp["gist"] + " - " + cala_time(chp["start"])):
            chp["summary"]

# save_transcript("19bb63e7d7ab4fd293999b0323c3b2bd", auto_chapters=True)
