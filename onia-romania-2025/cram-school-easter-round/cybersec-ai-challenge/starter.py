import pandas as pd
# === Read the data
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

# === Subtask 1
value_subtask1 = []  # subtask 1 answers
task1 = pd.DataFrame({
    'subtaskID': 1,
    'datapointID': df_test.ID,
    'answer':  value_subtask1
})

# === Subtask 2
y_pred = [] # Model predictions

task2 = pd.DataFrame({
    'subtaskID': 2,
    'datapointID': df_test.ID,
    'answer': y_pred
})

# === Final datatset
submission_df = pd.concat([task1, task2], ignore_index=True)
submission_df.to_csv("submission.csv", index=False)

