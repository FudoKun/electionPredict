# src/features.py

def add_features(result):
    # sorting by state and year to ensure shifting to prev-year results is easy
    result = result.sort_values(["state", "year"])

    # within each state, we should be able to grab prev-elections pct
    result["prev_dem_pct"] = result.groupby("state")["dem_pct"].shift(1)

    # adding incumbency for another factor. We will be hardcoding some factors that have only yearly values.
    incumbent_party = {
        1976: "REPUBLICAN",  # Ford
        1980: "DEMOCRAT",  # Carter
        1984: "REPUBLICAN",  # Reagan
        1988: "REPUBLICAN",  # Reagan's 2nd term -> Bush
        1992: "REPUBLICAN",  # Bush
        1996: "DEMOCRAT",  # Clinton
        2000: "DEMOCRAT",  # Clinton's 2nd term -> Gore
        2004: "REPUBLICAN",  # Bush
        2008: "REPUBLICAN",  # Bush's 2nd term -> McCain
        2012: "DEMOCRAT",  # Obama
        2016: "DEMOCRAT",  # Obama's 2nd term -> Hillary
        2020: "REPUBLICAN",  # Trump
    }

    result["incumbent_dem"] = result["year"].map(incumbent_party).map({"DEMOCRAT": 1, "REPUBLICAN": 0})
    result["avg_dem_pct"] = result.groupby("year")["dem_pct"].transform("mean")

    # Annual average inflation rate (CPI, %) — source: BLS via multpl.com
    inflation = {
        1976: 5.7, 1980: 13.5, 1984: 4.3, 1988: 4.1,
        1992: 3.0, 1996: 3.0, 2000: 3.4, 2004: 2.7,
        2008: 3.8, 2012: 2.1, 2016: 1.3, 2020: 1.2,
    }

    # Annual average unemployment rate (%) — source: BLS
    unemployment = {
        1976: 7.7, 1980: 7.2, 1984: 7.5, 1988: 5.5,
        1992: 7.5, 1996: 5.4, 2000: 4.0, 2004: 5.5,
        2008: 5.8, 2012: 8.1, 2016: 4.9, 2020: 8.1,
    }

    # Gallup presidential approval (%, approx. October before election)
    approval = {
        1976: 48,  # Ford
        1980: 37,  # Carter
        1984: 58,  # Reagan
        1988: 51,  # Reagan
        1992: 34,  # Bush Sr
        1996: 54,  # Clinton
        2000: 57,  # Clinton
        2004: 48,  # Bush Jr
        2008: 25,  # Bush Jr
        2012: 49,  # Obama
        2016: 53,  # Obama
        2020: 46,  # Trump
    }

    # National polling average — Dem two-party share (%)
    # Source: Gallup final estimate (1976-2012), RCP average (2016-2024)
    national_poll_dem = {
        1976: 49.5,  # Carter 48 vs Ford 49
        1980: 48.4,  # Carter 44 vs Reagan 47
        1984: 41.0,  # Mondale 41 vs Reagan 59
        1988: 44.0,  # Dukakis 44 vs Bush 56
        1992: 57.0,  # Clinton 49 vs Bush 37
        1996: 55.9,  # Clinton 52 vs Dole 41
        2000: 48.9,  # Gore 46 vs Bush 48
        2004: 50.0,  # Kerry 49 vs Bush 49
        2008: 55.6,  # Obama 55 vs McCain 44
        2012: 49.5,  # Obama 49 vs Romney 50
        2016: 51.8,  # Clinton 46.8 vs Trump 43.6
        2020: 52.3,  # Biden 51.4 vs Trump 46.9
        2024: 50.1,  # Harris 48.7 vs Trump 48.6
    }
    result["national_poll"] = result["year"].map(national_poll_dem)
    result["inflation"] = result["year"].map(inflation)
    result["unemployment"] = result["year"].map(unemployment)
    result["approval"] = result["year"].map(approval)
    # if incumbent dem then 1, good econ helps dems, if inc rep then -1 good econ hurts dems
    sign = result["incumbent_dem"] * 2 - 1

    # for approval, high approval helps so sign stays as is, for the other two high rates hurt, so negative sign.
    result["approval_effect"] = result["approval"] * sign
    result["inflation_effect"] = result["inflation"] * -sign
    result["unemployment_effect"] = result["unemployment"] * -sign
    return result
