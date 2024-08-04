import streamlit as st
import pandas as pd
import numpy as np
import update_map
import KOTR_update
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Team Page", 
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


team_options = team_names.insert(0, "None")
with st.sidebar:
    team_option = st.selectbox("Select a team to view stats: ", (team_names))
###
if team_option == "None":
    st.header("Select a team in the sidebar to view stats.")
else:
    team_score = st.session_state.overall_score.at["Score", team_option]

    score_t = st.session_state.overall_score.transpose()
    score_t = score_t.sort_values(by = "Score", ascending = False)
    position = score_t.index.get_loc(team_option) + 1

    region_summary = KOTR_update.team_tracking(st.session_state.team_region_ehp, team_option)

    if position == 1:
        position = "first"
    if position == 2:
        position = "second"
    if position == 3:
        position = "third"

    st.header(f"{team_option} is currently in {position} place with {team_score} points.")

    team_display = st.selectbox("Which table do you want to display?", [None, "Raw gains", "EHP gains", "Region totals", "Region leaderboard"])

    if team_display == None:
        st.markdown(":frog: ribbeth")
    if team_display == "Raw gains":
        team_delta_df = st.session_state.delta_df[st.session_state.delta_df["Team"] == team_option].drop(columns = ["Team"])
        team_delta_df = KOTR_update.add_total_row(team_delta_df)
        st.dataframe(team_delta_df, height = (len(team_delta_df) + 1) * 35 + 3)
    if team_display == "EHP gains":
        team_ind_ehp = st.session_state.individual_ehp[st.session_state.individual_ehp["Team"] == team_option].drop(columns = ["Team"])
        team_ind_ehp = KOTR_update.add_total_row(team_ind_ehp)
        st.dataframe(team_ind_ehp, height = (len(team_ind_ehp) + 1) * 35 + 3)
    if team_display == "Region totals":
        team_ind_region_ehp = st.session_state.individual_region_ehp[st.session_state.individual_region_ehp["Team"] == team_option].drop(columns = ["Team"])
        team_ind_region_ehp = KOTR_update.add_total_row(team_ind_region_ehp)
        st.dataframe(team_ind_region_ehp, height = (len(team_ind_region_ehp) + 1) * 35 + 3)
    if team_display == "Region leaderboard":
        st.dataframe(region_summary, height = (len(region_summary) + 1) * 35 + 3)