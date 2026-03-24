# src/data_loader.py
import pandas as pd

def load_and_clean():
    data = pd.read_csv("data/1976-2020-president.csv")

    filtered = data[
        ((data["party_simplified"] == "DEMOCRAT") | (data["party_simplified"] == "REPUBLICAN"))
        & (data["writein"] == False)
    ]

    result = filtered.pivot_table(index=["year", "state"], columns=["party_simplified"], values=["candidatevotes"])
    result.columns = ["dem_votes", "rep_votes"]
    result = result.reset_index()
    result["dem_pct"] = (result["dem_votes"] / (result["dem_votes"] + result["rep_votes"])) * 100

    return result