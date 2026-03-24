from src.data_loader import load_and_clean
from src.features import add_features
from src.model import backtest, make_prediction
from src.visualize import draw_map

result = load_and_clean()
result = add_features(result)
model_data = result.dropna(subset=["prev_dem_pct"])

backtest(model_data)
predictions = make_prediction(model_data, result)
draw_map(predictions)