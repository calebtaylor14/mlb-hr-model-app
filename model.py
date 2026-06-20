def calculate_hr_score(row):

    pitcher = (
        row["pitcher_hr9"] * 0.25 +
        row["pitcher_barrel_allowed"] * 0.20 +
        row["pitcher_flyball"] * 0.20 +
        row["pitcher_xslg"] * 0.35
    )

    batter = (
        row["barrel_pct"] * 0.30 +
        row["hardhit_pct"] * 0.25 +
        row["pull_air_pct"] * 0.30 +
        row["iso"] * 0.15
    )

    matchup = (
        row["pitch_type_edge"] +
        row["handedness_edge"] +
        row["swing_fit"]
    )

    suppression = row["pitcher_suppression"]

    environment = row["park_score"] + row["weather_score"]

    form = row["recent_form"]
    bullpen = row["bullpen_risk"]

    total = (
        pitcher +
        batter +
        matchup +
        suppression +
        environment +
        form +
        bullpen
    )

    return round(total, 2)
