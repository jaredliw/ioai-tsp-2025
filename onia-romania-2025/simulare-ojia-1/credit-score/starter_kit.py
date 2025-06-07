import pandas as pd



df_train = pd.read_csv('train_data.csv')
df_test = pd.read_csv('test_data.csv')


subtask1 = 'subtask1'
subtask2 = 'subtask2'
subtask3 = 'subtask3'
subtask4 = 'subtask4'
subtask5 = 'subtask5'


# === PRELUCRARE DATE

# === ANTRENARE MODEL
model = ''


# === PREDICTII (Subtask 5)
df_test[subtask5] = model.predict(df_test)

# === CONSTRUIRE FORMAT FINAL CSV
results = []

# Subtask 1–4: cate o valoare unica per subtask
# results.append((1, 1, val)
# results.append((2, 1, val)
# results.append((3, 1, val)
# results.append((4, 1, val)

# Subtask 5: fiecare rand din test
for row in df_test.itertuples():
    results.append((5, row.id, float(row.subtask5)))

df_output = pd.DataFrame(results, columns=['subtaskID', 'datapointID', 'answer'])
df_output.to_csv('final_submission.csv', index=False)


