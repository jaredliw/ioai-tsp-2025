import pandas as pd


df_train = pd.read_csv('train_data.csv')
df_test = pd.read_csv('test_data.csv')


subtask1 = 'mean_traffic_level'
subtask2 = 'std_traffic_level'
subtask3 = 'on_time'

#Defineste un model
# model
# Predictii model
# y_pred

# df_test[subtask3] = model.predict(df_test)

# Construiește rezultatul final
results = []

# Subtask 1 – un singur datapoint
# results.append((1, 1,  valoare))

# Subtask 2 – un singur datapoint
# results.append((2, 1, valoare))

# Subtask 3 – predicțiile pe test set
for row in df_test.itertuples():
    results.append((3, row.id, float(row.on_time)))

# Salveaza rezultatele
df_output = pd.DataFrame(results, columns=['subtaskID', 'datapointID', 'answer'])
df_output.to_csv('final_submission.csv', index=False)
