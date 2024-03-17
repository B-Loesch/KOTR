import streamlit as st
import pandas as pd
import update_map
import KOTR_update

path = "D:/Brandon Loesch/KOTR/KOTR/"

start_df = pd.read_pickle(f"{path}Start.pkl")
update_df = pd.read_pickle(f"{path}Update.pkl")
delta_df = update_df - start_df
ehp_df = pd.read_pickle(f"{path}EHP.pkl")

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
individual_region_ehp = KOTR_update.calc_individual_ehp_region(delta_df, region_dict)
team_region_ehp = individual_region_ehp.groupby(by = "Team").sum().transpose()
overall_score = KOTR_update.calc_overall_score(team_region_ehp)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", "Main", "Team1", "Team2", "Team3", "Individual Stats", "Test"])

with tab1:
    st.header("Welcome to King of the Region!")
    st.image(r"D:\Brandon Loesch\KOTR\trailblazer.png")

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
    KOTR_map = update_map.update_map("D:/Brandon Loesch/KOTR", team_region_ehp)
    st.image(KOTR_map)

    st.header("Team region score: ")
    st.dataframe(team_region_ehp.style.background_gradient(axis = 0), width = 800)

    st.header("Overall competition score: ")
    st.dataframe(overall_score.style.background_gradient(axis = 1), width = 800)

with tab3:
    st.text("This tab should show information for each team")
with tab4:
    st.text("This tab should show information for each team")
with tab5:
    st.text("This tab should show information for each team")

with tab6:
    st.text("This is the tab for individual stats.")
    st.dataframe(delta_df)
    st.dataframe(individual_ehp)
    st.dataframe(individual_region_ehp)
    
    # st.text("This table shows each participant's experience or kills for each category.")
    # st.dataframe(delta_df)

    # individual_ehp = pd.DataFrame(0, columns=delta_df.columns.tolist(), index = delta_df.index.tolist())
    # def calc_individual_ehp(cat):
    #     if cat == "Team":
    #         return(delta_df[cat])
    #     else:
    #         return(delta_df[cat] / ehp_df.at[cat, "EHP Rate"])
        
    # for cat in delta_df.columns.tolist():
    #     individual_ehp[cat] = calc_individual_ehp(cat)

    # st.text("This table shows each participant's ehp for each category.")
    # st.dataframe(individual_ehp)

    # regions = list(region_dict.keys())
    # regions.append("Team")
    # region_leaderboard_individual = pd.DataFrame(0, columns = delta_df.index.tolist(), index = regions)

    # def calc_region_ehp_individual(name):
    #     # Takes a teams' delta dataframe and returns a dictionary:
    #     # Keys are the region and values are the total ehp in that region
    #     region_ehp_dict = {}
    #     temp_df = delta_df.loc[name]
    #     for region in region_dict:
    #         region_ehp = 0
    #         for cat in region_dict[region]:           
    #             cat_ehp = delta_df.loc[name][cat] / ehp_df.at[cat, "EHP Rate"]
    #             region_ehp += cat_ehp
            
    #         region_ehp_dict[region] = region_ehp
            
    #     region_ehp_dict["Team"] = delta_df.at[name, "Team"]
        
    #     return(region_ehp_dict)

    # for name in delta_df.index.tolist():
    #     values = calc_region_ehp_individual(name)
    #     region_leaderboard_individual[name] = values
    # region_leaderboard_individual_transposed = region_leaderboard_individual.transpose()

    # st.text("This table shows each participant's summed ehp for each region.")
    # st.dataframe(region_leaderboard_individual_transposed)

    # region_leaderboard_team_transposed = region_leaderboard_individual_transposed.groupby(by = "Team").sum().transpose()
    # st.text("This table shows each team's summed ehp for each region.")
    # st.dataframe(region_leaderboard_team_transposed)

    # overall_score = pd.DataFrame(0, columns=[1, 2, 3], index = ["Score"])
    # for i in range(region_leaderboard_team_transposed.shape[0]):
    #     max_team = region_leaderboard_team_transposed.iloc[i,:].idxmax()
    #     min_team = region_leaderboard_team_transposed.iloc[i,:].idxmin()
        
    #     team_set = set(region_leaderboard_team_transposed.columns.tolist())
    #     mid_team = (team_set - {max_team}) - {min_team}
        
    #     mid_team = mid_team.pop() if mid_team else None
        
    #     overall_score[max_team] += 1
    #     overall_score[mid_team] += 0.5
    # st.text("This is the overall score for the competition.")
    # st.dataframe(overall_score)

    # region_leaderboard_team_transposed.columns = ["Semen Demons", "Guthix Gooch", "Morytania Meatflaps"]
    # KOTR_map = update_map.update_map("D:/Brandon Loesch/KOTR", region_leaderboard_team_transposed)
    # st.image(KOTR_map)


