import pandas as pd
from sklearn.metrics import mean_absolute_error


# Aceasta este functia de evaluare care calculeaza scorul T2, in functie de metrica MAE trimisa ca parametru.
# Puteti astfel sa intelegeti care ar trebui sa fie MAE-ul pentru care ar trebui sa obtineti un scor maxim.
def evaluate_t2_score(mae):
    import numpy as np
    # Interpolation such that at min_value you get score_min, at max_value you get score_max
    def lerp(value, min_value, max_value, score_min, score_max) -> int:
        slide = np.clip((value - min_value) / (max_value - min_value), 0.0, 1.0)
        score_res = score_min + (score_max - score_min) * slide
        return int(score_res)

    score = 0
    if mae >= 100:
        score = 0
    elif mae >= 20:
        score = lerp(mae, 100.0, 20.0, 0, 10)
    elif mae >= 10.0:
        score = lerp(mae, 20.0, 10.0, 10, 30)
    elif mae >= 8.0:
        score = lerp(mae, 10.0, 8.0, 30, 40)
    elif mae >= 5.0:
        score = lerp(mae, 8.0, 5.0, 40, 60)
    elif mae >= 4.5:
        score = lerp(mae, 5.0, 4.5, 60, 70)
    else:
        score = lerp(mae, 4.5, 4.3, 70, 80)

    return score, mae, score, mae


# Citirea datelor
train_df = pd.read_csv("train_data.csv")
predict_df = pd.read_csv("test_data.csv")

# Testam daca se incarca corect
print("Train DataFrame:", train_df.head())




