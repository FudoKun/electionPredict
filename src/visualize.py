# src/visualize.py
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def draw_map(predictions):
    us = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")

    us["name_upper"] = us["name"].str.upper()
    map_data = us.merge(predictions[["state", "predicted_dem", "predicted_winner"]],
                        left_on="name_upper", right_on="state", how="left")

    norm = mcolors.TwoSlopeNorm(vmin=35, vcenter=50, vmax=65)
    cmap = mcolors.LinearSegmentedColormap.from_list("rb", ["red", "white", "blue"])

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    map_data.plot(column="predicted_dem", cmap=cmap, norm=norm,
                  linewidth=0.5, edgecolor="black", ax=ax)
    ax.set_title("2024 Presidential Election — Model Prediction", fontsize=16)
    ax.axis("off")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=ax, shrink=0.5, label="Democratic Two-Party Vote Share (%)")
    plt.savefig("2024_prediction_map.png", dpi=150, bbox_inches="tight")
    plt.show()