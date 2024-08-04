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

###
players = sorted(name_list, key = str.casefold)
players.insert(0, "None")


use_region_df = st.session_state.individual_region_ehp.drop(["Total",])
use_region_df['Total'] = use_region_df.drop(columns='Team', errors='ignore').sum(axis = 1)
use_region_df = use_region_df[["Total"] + [col for col in use_region_df.columns if col != "Total"]]


use_individual_df = st.session_state.individual_ehp.drop(["Total",])
use_individual_df['Total'] = use_individual_df.drop(columns='Team', errors='ignore').sum(axis = 1)
use_individual_df = use_individual_df[["Total"] + [col for col in use_individual_df.columns if col != "Total"]]

with st.sidebar:
    name_selection = st.selectbox("Select a player to highlight: ", (players))
    # st.text(f"{name_selection} has gained {use_individual_df.loc[name_selection].sum(axis=0)} ehp.")

st.text("This is the page for individual stats. Select a player in the sidebar to highlight their stats.")
with st.container(border = True):
    st.header("Region Leaderboard")
    st.dataframe(KOTR_update.region_leaderboard(use_region_df).style.map(lambda x: "background-color: blue" if x == name_selection else None))
with st.container(border = True):
    st.header("EHP gained in each region.")
    ind_reg_ehp_total = use_region_df
    st.dataframe(ind_reg_ehp_total.style.apply(lambda x: ["background-color: blue" if x.name == name_selection else '' for i in x], axis=1))
with st.container(border = True):
    st.header("EHP gained in each category.")
    st.dataframe(use_individual_df.style.apply(lambda x: ["background-color: blue" if x.name == name_selection else '' for i in x], axis=1))

