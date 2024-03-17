import pandas as pd
import numpy as np
import requests

path = "D:/Brandon Loesch/KOTR/KOTR/"
ehp_df = pd.read_pickle(f"{path}EHP.pkl")

def calc_individual_ehp(delta_df, ehp_df):
    # Generates the individual ehp dataframe given the delta dataframe
    individual_ehp = pd.DataFrame(0, columns=delta_df.columns.tolist(), index = delta_df.index.tolist())
    for cat in delta_df.columns.tolist():
        if cat == "Team":
            individual_ehp[cat] == delta_df[cat]
        else:
            individual_ehp[cat] = delta_df[cat] / ehp_df.at[cat, "EHP Rate"]
    
    return(individual_ehp)

def calc_individual_ehp_region(delta_df, region_dict):
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
