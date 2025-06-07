import pandas as pd

# Încărcare date de antrenament
df_antrenament = pd.read_csv('train_data.csv')

# Obținere rezultate pentru p1, p2, p3, p4

# Inițializare dataframe pentru răspunsuri
output = {
    'subtaskID': [1, 2, 3, 4],
    'datapointID': [1, 1, 1, 1],
    'answer': [0, 0, 0, 0]
}
df_raspunsuri = pd.DataFrame(output)

# Antrenare model ...
# (Aici ar trebui să fie codul de antrenare al modelului)

# Încărcare date de test
df_test = pd.read_csv("test_data.csv")

# Extragere date pentru subtask-ul 5
filtrat_pentru_p5 = df_test[df_test['Subtask'] == 5]

# Predicția cu modelul antrenat pentru fiecare utilizator din setul de test pentru p5
for _, rand in filtrat_pentru_p5.iterrows():
    
    # Predicția
    predictie = 89  # Exemplu de predicție fixă, înlocuiește cu predicția reală

    # Salvarea rezultatului
    rand_nou = {
        'subtaskID': 5,
        'datapointID': int(rand['User_ID']),
        'answer': predictie
    }
    df_raspunsuri = pd.concat([df_raspunsuri, pd.DataFrame([rand_nou])], ignore_index=True)

# Extragere date pentru subtask-ul 6
filtrat_pentru_p6 = df_test[df_test['Subtask'] == 6]

# Predicția cu modelul antrenat pentru fiecare utilizator din setul de test pentru p6
for _, rand in filtrat_pentru_p6.iterrows():
    
    # Predicția
    predictie = 89  # Exemplu de predicție fixă, înlocuiește cu predicția reală

    # Salvarea rezultatului
    rand_nou = {
        'subtaskID': 6,
        'datapointID': int(rand['User_ID']),
        'answer': predictie
    }
    df_raspunsuri = pd.concat([df_raspunsuri, pd.DataFrame([rand_nou])], ignore_index=True)

# Salvare răspunsuri în fișier CSV
df_raspunsuri.to_csv('sample_output.csv', index=False)
