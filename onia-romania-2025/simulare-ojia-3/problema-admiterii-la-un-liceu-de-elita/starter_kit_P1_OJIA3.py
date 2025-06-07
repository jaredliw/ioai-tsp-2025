# Starter kit

import pandas as pd

[IMPORT LIBRARII]

df_train = pd.read_csv('train_data.csv')
df_test = pd.read_csv('test_data.csv')

subtask1 ='dif_NT-MEV'
subtask2='loc-MEV'
subtask3='status_admitere'

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

train, validation = train_test_split(df_train, test_size=0.2, random_state=0)

y_train = train[subtask3]
X_train = train.drop(columns=[subtask3])

y_validation = validation[subtask3]
X_validation = validation.drop(columns=[subtask3])

[INSERT CORECTARE / CURATARE DATE]
[INSERT ANTRENARE PE TRAIN SI VALIDATION]
[STANDARDIZARE COLOANE NUMERICE]

model = model.fit(X_train, y_train)
y_pred = model.predict(X_validation)
print(accuracy_score(y_pred, y_validation))

df_test[subtask1] = [CALCULUL CERUT LA SUBTASK 1]
df_test[subtask2] = [CALCULUL CERUT LA SUBTASK 2]
df_test[subtask3] = model.predict(df_test)
df_test[['id', subtask1, subtask2, subtask3]].to_csv('output.csv', index=False)
