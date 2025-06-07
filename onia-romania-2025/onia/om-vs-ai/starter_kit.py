import pandas as pd
import numpy as np

# === citire date
train_df = pd.read_csv("train_data.csv")
test_df = pd.read_csv("test_data.csv")

submission = []




# === Subtask 1
train_sub1 = train_df.copy()


# test_sub1["answer"] = [lista cu raspunsuri]

# Adauga in submisie submisie
submission.append(test_sub1[["subtaskID", "ID", "answer"]].rename(columns={"ID": "datapointID"}))

# === Subtask 2
test_sub2 = test_df[test_df["subtaskID"] == 2].copy()

# Adauga in submisie submisie
# test_sub2["answer"] = [lista cu raspunsuri]

# Adaugă în submisie
submission.append(test_sub2[["subtaskID", "ID", "answer"]].rename(columns={"ID": "datapointID"}))

# === Salveaza submisia
final_submission = pd.concat(submission, ignore_index=True)
final_submission.to_csv("submission.csv", index=False)
