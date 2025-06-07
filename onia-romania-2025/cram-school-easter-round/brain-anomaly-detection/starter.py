import pandas as pd
import numpy as np


# === Read the date
df_train = pd.read_csv("processed_train.csv",  dtype={"id": str})
df_test = pd.read_csv("processed_test.csv",  dtype={"id": str})

# === Extract photo
df_train["pixels"] = df_train["pixels"].apply(eval)
df_test["pixels"] = df_test["pixels"].apply(eval)

# === Subtask 1

subtask1_rows = []
for i, row in df_train.iterrows():
    vector = np.array(row["pixels"])
    subtask1_rows.append((1, row["id"], "value"))

# === Subtask 2
X_test = np.vstack(df_test["pixels"].values)
y_train = df_train["class"]

y_pred = [] # values
subtask2_rows = []
for id_, pred in zip(df_test["id"], y_pred):
    subtask2_rows.append((2, id_, 0))

# === Final submission
submission_rows = subtask1_rows + subtask2_rows
df_submission = pd.DataFrame(submission_rows, columns=["subtaskID", "datapointID", "answer"])
df_submission.to_csv("submission.csv", index=False)

