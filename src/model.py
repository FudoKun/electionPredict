# src/model.py
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

FEATURES = ["prev_dem_pct", "incumbent_dem", "national_poll", "approval_effect", "inflation_effect", "unemployment_effect"]

ELECTORAL_VOTES = {
    "ALABAMA": 9, "ALASKA": 3, "ARIZONA": 11, "ARKANSAS": 6,
    "CALIFORNIA": 54, "COLORADO": 10, "CONNECTICUT": 7, "DELAWARE": 3,
    "DISTRICT OF COLUMBIA": 3, "FLORIDA": 30, "GEORGIA": 16, "HAWAII": 4,
    "IDAHO": 4, "ILLINOIS": 19, "INDIANA": 11, "IOWA": 6,
    "KANSAS": 6, "KENTUCKY": 8, "LOUISIANA": 8, "MAINE": 4,
    "MARYLAND": 10, "MASSACHUSETTS": 11, "MICHIGAN": 15, "MINNESOTA": 10,
    "MISSISSIPPI": 6, "MISSOURI": 10, "MONTANA": 4, "NEBRASKA": 5,
    "NEVADA": 6, "NEW HAMPSHIRE": 4, "NEW JERSEY": 14, "NEW MEXICO": 5,
    "NEW YORK": 28, "NORTH CAROLINA": 16, "NORTH DAKOTA": 3, "OHIO": 17,
    "OKLAHOMA": 7, "OREGON": 8, "PENNSYLVANIA": 19, "RHODE ISLAND": 4,
    "SOUTH CAROLINA": 9, "SOUTH DAKOTA": 3, "TENNESSEE": 11, "TEXAS": 40,
    "UTAH": 6, "VERMONT": 3, "VIRGINIA": 13, "WASHINGTON": 12,
    "WEST VIRGINIA": 4, "WISCONSIN": 10, "WYOMING": 3,
}


def backtest(model_data):
    lr_model = LinearRegression()
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    years = sorted(model_data["year"].unique())

    for test_year in years:
        if test_year == 1980:
            continue
        train = model_data[model_data["year"] < test_year]
        test = model_data[model_data["year"] == test_year]

        lr_model.fit(train[FEATURES], train["dem_pct"])
        lr_pred = lr_model.predict(test[FEATURES])
        lr_mae = (abs(lr_pred - test["dem_pct"].values)).mean()

        rf_model.fit(train[FEATURES], train["dem_pct"])
        rf_pred = rf_model.predict(test[FEATURES])
        rf_mae = (abs(rf_pred - test["dem_pct"].values)).mean()

        ensemble_pred = (lr_pred + rf_pred) / 2
        ens_mae = (abs(ensemble_pred - test["dem_pct"].values)).mean()

        print(f"{test_year}: LR = {lr_mae:.2f}  |  RF = {rf_mae:.2f}  |  ENS = {ens_mae:.2f}")


def make_prediction(model_data, result):
    lr_model = LinearRegression()
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

    preds = result[result["year"] == 2020][["state", "dem_pct"]].copy()
    preds = preds.rename(columns={"dem_pct": "prev_dem_pct"})
    preds["incumbent_dem"] = 1
    preds["national_poll"] = 50.1
    preds["approval_effect"] = 41 * 1
    preds["inflation_effect"] = 2.9 * -1
    preds["unemployment_effect"] = 4.0 * -1

    lr_model.fit(model_data[FEATURES], model_data["dem_pct"])
    rf_model.fit(model_data[FEATURES], model_data["dem_pct"])

    lr_pred = lr_model.predict(preds[FEATURES])
    rf_pred = rf_model.predict(preds[FEATURES])
    preds["predicted_dem"] = (lr_pred + rf_pred) / 2
    preds["predicted_winner"] = preds["predicted_dem"].apply(lambda x: "DEM" if x > 50 else "REP")

    print("\n=== 2024 SWING STATE PREDICTIONS ===")
    swing = preds[preds["predicted_dem"].between(45, 55)].sort_values("predicted_dem")
    print(swing[["state", "predicted_dem", "predicted_winner"]].to_string(index=False))

    preds["ev"] = preds["state"].map(ELECTORAL_VOTES)
    dem_ev = preds[preds["predicted_dem"] > 50]["ev"].sum()
    rep_ev = preds[preds["predicted_dem"] <= 50]["ev"].sum()
    print(f"\nDEM: {dem_ev} electoral votes")
    print(f"REP: {rep_ev} electoral votes")
    print(f"Winner: {'DEM' if dem_ev >= 270 else 'REP'}")
    #Since modelling Maine and NE district splits would require incorporating statewide polling, this doesn't do so yet.
    print(f"(Note: ME/NE district splits not modeled)")

    return preds