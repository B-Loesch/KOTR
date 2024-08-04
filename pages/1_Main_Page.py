import streamlit as st
import pandas as pd
import numpy as np
import update_map
import KOTR_update
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Main Competition Page", 
                   page_icon="📊",
                   layout = "wide")

team_names = ["Semen Demons", "Guthix Gooch", "Morytania Meatflaps"]

team1 = ['stinky metz',
  'TOaBundy',
  'Azbirddog',
  'dwaggleim',
  'The Maher',
  'FarmboyFrank',
  'rez',
  'Zalcanussy',
  'plusblastbtw',
  'lord uhlen']

team2 = ['wimen',
  'stjonkbonk',
  'Euxy',
  'skoomadrinke',
  'MIND THE WAP',
  'Quinninho',
  'Glish',
  'jinxtheminxx',
  'ChikitaChina',
  'Jonte xu2']

team3 = ['smallblue0',
  'Suitabl3',
  'IAmDivine',
  'Cramolix',
  'yankees fan7',
  'fleshrat',
  'gim alone',
  'Toyo Harada',
  'aged whale',
  'ThePoggest']

name_list = team1 + team2 + team3

team_colors = {team_names[0]: (255,255,255),
              team_names[1]: (0,255,0),
              team_names[2]: (100,0,100)}

plotly_team_colors = {team_names[0]: '#FFFFFF',
              team_names[1]: '#05FF00',
              team_names[2]: '#C000FF'}

comp_cols = ["Woodcutting EXP", "Fishing EXP", "Mining EXP", "Agility EXP", "Thieving EXP", "Slayer EXP",
                       "Farming EXP", "Runecrafting EXP", "Hunter EXP", "Abyssal Sire", 
                       "Alchemical Hydra", "Artio", "Barrows Chests", "Callisto", "Calvarion", "Cerberus", 
                       "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Chaos Elemental", "Commander Zilyana", 
                       "Corporeal Beast", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme",
                       "Duke Sucellus", "General Graardor", "Giant Mole", "Grotesque Guardians", 
                       "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", "Lunar Chests",
                       "Nex", "Phosani's Nightmare",
                       "Phantom Muspah", "Sarachnis", "Scorpia", "Scurrius", "Sol Heredit","Spindel", "Tempoross", 
                       "The Corrupted Gauntlet", "The Leviathan","The Whisperer", "Theatre of Blood", 
                       "Theatre of Blood: Hard Mode", "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                       "TzKal-Zuk", "TzTok-Jad", "Vardorvis", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah"]

region_dict = {"Tirannwn": ["Woodcutting EXP", "Zulrah", "Zalcano", "The Corrupted Gauntlet"],
              "Fremennik": ["Mining EXP", "Vorkath", "Phantom Muspah", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme", "Duke Sucellus"],
              "Kandarin": ["Fishing EXP", "Kraken", "Cerberus", "Thermonuclear Smoke Devil"],
              "Morytania": ["Agility EXP", "Barrows Chests", "Grotesque Guardians", "Phosani's Nightmare", "Theatre of Blood", "Theatre of Blood: Hard Mode"],
              "Karamja": ["Slayer EXP", "TzKal-Zuk", "TzTok-Jad"],
              "Wilderness": ["Callisto", "Calvarion", "Corporeal Beast", "Scorpia", "Venenatis", "Vet'ion", "King Black Dragon", "Artio", "Spindel", "Chaos Elemental"],
              "Zeah": ["Farming EXP", "Alchemical Hydra", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Sarachnis", "Wintertodt", "Vardorvis", "Lunar Chests", "Sol Heredit"],
              "Desert": ["Thieving EXP", "Kalphite Queen", "Tombs of Amascut", "Tombs of Amascut: Expert Mode", "Tempoross"],
              "Misthalin": ["Runecrafting EXP", "Abyssal Sire", "Giant Mole", "Scurrius", "The Whisperer", "The Leviathan"],
               "Asgarnia": ["Hunter EXP", "Kree'Arra", "General Graardor", "K'ril Tsutsaroth", "Nex", "Commander Zilyana"]}

### page specific code

KOTR_map = update_map.update_map("https://github.com/B-Loesch/KOTR/blob/main/Data/trailblazer.png?raw=true", st.session_state.team_region_ehp, team_colors)
st.header("Competition Map")
st.image(KOTR_map)

st.header("Overall Score")
with st.container(border=True):
    cols = st.columns(3)
    for i in range(3):
        col = cols[i]
        controlled_regions = []
        for index in st.session_state.team_region_ehp.index:
            if st.session_state.team_region_ehp.loc[index].idxmax(axis = "index") == st.session_state.team_region_ehp.columns[i]:
                controlled_regions.append(index)
        with col: 
            st.metric(f"{str(st.session_state.overall_score.columns[i])}:", f"{st.session_state.overall_score.iloc[0,i]} points", ' | '.join(controlled_regions))

st.header("Team region score: ")
with st.container(height = 550, border=True):
    selection = "All"
    selections = st.session_state.team_region_ehp.index.tolist()
    selections.insert(0, "All")
    selection = st.selectbox("Which region do you want to display?", sorted(selections))

    col1, col2 = st.columns(2)
    with col1:
        if selection == "All":
            st.session_state.team_region_ehp.loc["Total"] = st.session_state.team_region_ehp.sort_index().sum()
            st.dataframe(st.session_state.team_region_ehp.style.background_gradient(cmap = 'Blues', axis = 1), width = 500, height = 500)
        else: 
            st.dataframe(st.session_state.team_region_ehp.loc[[selection],:].style.background_gradient(cmap = 'Blues', axis = 1), width = 500)

            maxes = st.session_state.individual_region_ehp[selection].max()
            less_than_max = st.session_state.individual_region_ehp[selection].where(st.session_state.individual_region_ehp[selection].lt(maxes, axis='rows'))
            seconds = less_than_max.max()

            st.metric(f"{selection} MVP:", f"{st.session_state.individual_region_ehp[selection].idxmax()} - {round(st.session_state.individual_region_ehp[selection].max(), 2)} EHP", f"{round(maxes - seconds, 2)} hours")
    with col2:
        fig = KOTR_update.region_score_plotly(st.session_state.team_region_ehp, selection, plotly_team_colors, width = 600, height = 400)
        st.plotly_chart(fig, theme = "streamlit")