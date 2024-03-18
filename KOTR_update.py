import pandas as pd
import numpy as np
import requests

def get_hiscores_data(name_list):
    # Scrapes OSRS hiscores for each player and returns a dataframe
    # This can be used for competition initialization or for competition updates
    hiscores_df = pd.DataFrame()
    for player_name in name_list:
        url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={player_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode("utf-8")
            lines = data.split("\n")
            hiscores_data = [line.split(",") for line in lines if line.strip()]
            columns = ["skill", "rank", "level"]
            df = pd.DataFrame(hiscores_data, columns=columns)
            df.set_index("skill", inplace=True)
            df = pd.DataFrame(df.stack()).T
            df.columns = df.columns.map("_".join)
            df.index = [player_name]
            df.columns = ["Total", "Total EXP", "Attack", "Attack EXP", "Defence", "Defence EXP", "Strength", "Strength EXP", "Hitpoints", "Hitpoints EXP", "Ranged", "Ranged EXP", "Prayer", "Prayer EXP", "Magic", "Magic EXP", "Cooking", "Cooking EXP", "Woodcutting", "Woodcutting EXP",
                    "Fletching", "Fletching EXP", "Fishing", "Fishing EXP", "Firemaking", "Firemaking EXP", "Crafting", "Crafting EXP", "Smithing", "Smithing EXP", "Mining", "Mining EXP", "Herblore", "Herblore EXP", "Agility", "Agility EXP", "Thieving", "Thieving EXP", "Slayer", "Slayer EXP",
                    "Farming", "Farming EXP", "Runecrafting", "Runecrafting EXP", "Hunter", "Hunter EXP", "Construction", "Construction EXP", "blank1", "League Points", "Bounter Hunter - Hunter", "Bountry Hunter - Rogue", "Bounter Hunter - Hunter (Legacy)", "Bountry Hunter - Rogue (Legacy)","Clue Scrolls (all)", "Clue Scrolls (beginner)", "Clue Scrolls (easy)", "Clue Scrolls (medium)",
                    "Clue Scrolls (hard)", "Clue Scrolls (elite)", "Clue Scrolls (master)", "LMS - Rank", "Soul Wars Zeal", "PVP Arena - Rank", "Guardians of the Rift - Rifts Closed", "Abyssal Sire", "Alchemical Hydra", "Artio", "Barrows Chests", "Bryophyta",
                    "Callisto", "Calvarion", "Cerberus", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Chaos Elemental", "Chaos Fanatic", "Commander Zilyana", "Corporeal Beast", "Crazy Archaeologist", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme",
                    "Deranged Archaeologist", "Duke Sucellus","General Graardor", "Giant Mole", "Grotesque Guardians", "Hespori", "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", "Mimic", "Nex", "Nightmare", "Phosani's Nightmare", "Obor",
                    "Phantom Muspah", "Sarachnis", "Scorpia", "Scurrius", "Skotizo", "Spindel", "Tempoross", "The Gauntlet", "The Corrupted Gauntlet", "The Leviathan","The Whisperer","Theatre of Blood", "Theatre of Blood: Hard Mode", "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                    "TzKal-Zuk", "TzTok-Jad", "Vardorvis", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah"]
        if df is not None:
            hiscores_df = pd.concat([hiscores_df, df], axis = 0)
        
    return(hiscores_df)

def calc_individual_ehp(delta_df, ehp_df):
    # Generates the individual ehp dataframe given the delta dataframe
    individual_ehp = pd.DataFrame(0, columns=delta_df.columns.tolist(), index = delta_df.index.tolist())
    for cat in delta_df.columns.tolist():
        if cat == "Team":
            individual_ehp[cat] == delta_df[cat]
        else:
            individual_ehp[cat] = delta_df[cat] / ehp_df.at[cat, "EHP Rate"]
    
    return(individual_ehp)

def calc_individual_ehp_region(delta_df, region_dict, ehp_df):
    # Generates the region ehp datafrane given the delta dataframe
    regions = ["Tirannwn", "Fremennik", "Kandarin", "Morytania", "Karamja", "Wilderness", "Zeah", "Desert", "Misthalin", "Asgarnia"]
    regions.append("Team")
    region_leaderboard_individual = pd.DataFrame(0, columns = delta_df.index.tolist(), index = regions)
    
    for name in delta_df.index.tolist():
        region_ehp_dict = {}
        for region in region_dict:
            region_ehp = 0
            for cat in region_dict[region]:
                cat_ehp = delta_df.loc[name][cat] / ehp_df.at[cat, "EHP Rate"]
                region_ehp += cat_ehp
            
            region_ehp_dict[region] = region_ehp

        region_ehp_dict["Team"] = delta_df.at[name, "Team"]
        values = region_ehp_dict

        region_leaderboard_individual[name] = values

    return(region_leaderboard_individual.transpose())

def calc_overall_score(team_region_ehp):
    overall_score = pd.DataFrame(0, columns=[1, 2, 3], index = ["Score"])
    for i in range(team_region_ehp.shape[0]):
        max_team = team_region_ehp.iloc[i, :].idxmax()
        min_team = team_region_ehp.iloc[i, :].idxmin()

        team_set = set(team_region_ehp.columns.tolist())
        mid_team = (team_set - {max_team}) - {min_team}
        mid_team = mid_team.pop() if mid_team else None

        overall_score[max_team] += 1
        overall_score[mid_team] += 1

    return(overall_score)
