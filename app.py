import streamlit as st
import pandas as pd
import update_map
import KOTR_update
import matplotlib as plt

path = "D:/Brandon Loesch/KOTR/KOTR/"

comp_cols = ["Woodcutting EXP", "Fishing EXP", "Mining EXP", "Agility EXP", "Thieving EXP", "Slayer EXP",
                       "Farming EXP", "Runecrafting EXP", "Hunter EXP", "Abyssal Sire", 
                       "Alchemical Hydra", "Artio", "Barrows Chests", "Callisto", "Calvarion", "Cerberus", 
                       "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Chaos Elemental", "Commander Zilyana", 
                       "Corporeal Beast", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme",
                       "Duke Sucellus", "General Graardor", "Giant Mole", "Grotesque Guardians", 
                       "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", 
                       "Nex", "Phosani's Nightmare",
                       "Phantom Muspah", "Sarachnis", "Scorpia", "Scurrius", "Spindel", "Tempoross", 
                       "The Corrupted Gauntlet", "The Leviathan","The Whisperer", "Theatre of Blood", 
                       "Theatre of Blood: Hard Mode", "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                       "TzKal-Zuk", "TzTok-Jad", "Vardorvis", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah"]

start_df = pd.read_csv("https://raw.githubusercontent.com/B-Loesch/KOTR/main/Data/Start.csv?token=GHSAT0AAAAAACOV5CJF34IDVJZDS2O3F6VSZPXP6AQ").set_index("Username")

update_df = pd.read_csv("https://raw.githubusercontent.com/B-Loesch/KOTR/main/Data/Update.csv?token=GHSAT0AAAAAACOV5CJEWD2UZICAABQ66QTGZPXP6KA").drop(columns=["Time"]).set_index("Username")

ehp_df = pd.read_csv("https://raw.githubusercontent.com/B-Loesch/KOTR/main/Data/EHP.csv?token=GHSAT0AAAAAACOV5CJFODAKFK6JRVWSZUJAZPXP5SA").set_index("Category")
ehp_df["EHP Rate"] = ehp_df["EHP Rate"].astype(float)

cols_to_add = ["Artio", "Calvarion", "Duke Sucellus", "Scurrius", "Spindel", "The Leviathan", "The Whisperer", "Vardorvis"]
for col in cols_to_add:
    if col not in start_df:
        start_df[col] = 0
        update_df[col] = 0

start_df = start_df[comp_cols].astype(float).replace(-1, 0)
update_df = update_df[comp_cols].astype(float).replace(-1, 0)
delta_df = update_df - start_df

team1 = ["CmmandoSpork",
"Dezerthuntar",
"wha who",
"Blazeuchija",
"bowfabundy",
"OJdaInnocent",
"Lordcardhock ",
"Jack Da Rips",
"Doc Beeb",
"ImMaxy",
"Odd_mobile",
"Jaamies97",
"Iron My Cat",
"smallblue0",
"cwob",
"Jubnon"]

team2 = ["Mas3",
"Kobenaa",
"tits n rice",
"ITrimGlories",
"Yungllef",
"Quinninho",
"stjonkbonk",
"WolfAndSpice",
"Scoob x",
"maior ratio",
"J Mercs",
"Kano wins",
"Yankees fan7",
"Boarder21",
"goethium",
"Chikitichina"]

team3 = ["The Maher",
"Dusted Yuna",
"The 0racle",
"Bommerche",
"euxy",
"MrsWllw",
"Willowfi",
"Suitabl3",
"Im Folly",
"Plssmissile",
"Azbirddog",
"Sonfish",
"wimen",
"Key Concept",
"not2fly",
"Dr snuggles0"]

for name in start_df.index:
    if name in team1:
        delta_df.at[name, "Team"] = 1
    elif name in team2:
        delta_df.at[name, "Team"] = 2
    else:
        delta_df.at[name, "Team"] = 3

df_1 = delta_df[delta_df["Team"] == 1]
df_2 = delta_df[delta_df["Team"] == 2]
df_3 = delta_df[delta_df["Team"] == 3]

df_list = [df_1, df_2, df_3]

region_dict = {"Tirannwn": ["Woodcutting EXP", "Zulrah", "Zalcano", "The Corrupted Gauntlet"],
              "Fremennik": ["Mining EXP", "Vorkath", "Phantom Muspah", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme", "Duke Sucellus"],
              "Kandarin": ["Fishing EXP", "Kraken", "Cerberus", "Thermonuclear Smoke Devil"],
              "Morytania": ["Agility EXP", "Barrows Chests", "Grotesque Guardians", "Phosani's Nightmare", "Theatre of Blood", "Theatre of Blood: Hard Mode"],
              "Karamja": ["Slayer EXP", "TzKal-Zuk", "TzTok-Jad"],
              "Wilderness": ["Callisto", "Calvarion", "Corporeal Beast", "Scorpia", "Venenatis", "Vet'ion", "King Black Dragon", "Artio", "Spindel", "Chaos Elemental"],
              "Zeah": ["Farming EXP", "Alchemical Hydra", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Sarachnis", "Wintertodt", "Vardorvis"],
              "Desert": ["Thieving EXP", "Kalphite Queen", "Tombs of Amascut", "Tombs of Amascut: Expert Mode", "Tempoross"],
              "Misthalin": ["Runecrafting EXP", "Abyssal Sire", "Giant Mole", "Scurrius", "The Whisperer", "The Leviathan"],
               "Asgarnia": ["Hunter EXP", "Kree'Arra", "General Graardor", "K'ril Tsutsaroth", "Nex", "Commander Zilyana"]}

individual_ehp = KOTR_update.calc_individual_ehp(delta_df, ehp_df)
individual_region_ehp = KOTR_update.calc_individual_ehp_region(delta_df, region_dict, ehp_df)
team_region_ehp = individual_region_ehp.groupby(by = "Team").sum().transpose()
overall_score = KOTR_update.calc_overall_score(team_region_ehp)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", "Main", "Team1", "Team2", "Team3", "Individual Stats", "Test"])

with tab1:
    st.header("Welcome to King of the Region!")
    st.image("https://github.com/B-Loesch/KOTR/blob/main/Data/trailblazer.png?raw=true")

    st.write("Point are earned by gaining the most (or second most) combined EHB/EHP in a region - 1 point is awarded to first and 0.5 points are awarded to second, third place gets nothing. EHB/EHP rates are listed below, as well as which activity belongs to each region. Carefully make sure the content you are doing will count, if an activity is not listed it will not count for this competition! The team that obtains the most points will be considered the winner of the competition.")
    
    options = ehp_df["Region"].drop_duplicates().tolist()
    options.sort()
    option = st.selectbox("Region Categories and EHP: ", (options))
    st.dataframe(ehp_df[ehp_df["Region"] == option].drop(columns = ["Region"]), width = 800)

    st.write("The use of any PvM or skilling services during the competition is not permitted. The person who signs up for the competition must be the person to play the account and gain experience/KC/boss drops to be eligible to contribute. Boosting of any kind is also not permitted (eg Corp boosting/Essence running). For this competition, alts are allowed in all forms and uses. 6 hour logs are not permitted before the start of the competition. All participants will need to re-log just prior to comp start. Additionally, the following are not permitted to be used during the competition: - Pre-banked experience (including, but not limited to, brimhaven agility tickets, ores stored in blast mine, exp lamps, glistening tears etc.) - Holding chest/other rewards before comp start e.g. CoX, ToB, Corrupted Gauntlet, Wintertodt crates, Tempoross reward points, - Pre-banked clue caskets where the competition awards points for clues")
    st.write("As a general rule of thumb, content that is meant to be counted for the competition must be done during the competition. Anyone breaking this rule will be disqualified.")
    st.write("This dashboard will scrape the hiscores once every hour to update players' gains and update the scoring. Once the competition begins, players CAN NOT change their name.")
    

    
with tab2:
    st.text("This tab should show the overall hiscores, region hiscores, updated maps and figures")
    team_region_ehp.columns = ["Semen Demons", "Guthix Gooch", "Morytania Meatflaps"]
    KOTR_map = update_map.update_map("https://github.com/B-Loesch/KOTR/blob/main/Data/trailblazer.png?raw=true", team_region_ehp)
    st.image(KOTR_map)

    st.header("Team region score: ") #generate plots
    st.dataframe(team_region_ehp.style.background_gradient(axis = 0), width = 800)

    st.header("Overall competition score: ") # generate plots
    st.dataframe(overall_score.style.background_gradient(axis = 1), width = 800)

with tab3:
    st.text("This tab should show information for each team")
    # dataframe with team members and their total hours
    # dataframe with regions and hours - as well as hours behind first and second
with tab4:
    st.text("This tab should show information for each team")
    # dataframe with team members and their total hours
    # dataframe with regions and hours - as well as hours behind first and second
with tab5:
    st.text("This tab should show information for each team")
    # dataframe with team members and their total hours
    # dataframe with regions and hours - as well as hours behind first and second

with tab6:
    st.text("This is the tab for individual stats.")
    st.dataframe(delta_df)
    st.dataframe(individual_ehp)
    st.dataframe(individual_region_ehp)


