# Importăm biblioteca pandas pentru a manipula datele
import pandas as pd 

# Citim fișierul CSV cu datele de antrenament și afișăm primele 5 rânduri
df_train = pd.read_csv('train_data.csv')
print(df_train.head())

# Citim fișierul CSV cu datele de test și afișăm primele 5 rânduri
df_test = pd.read_csv('test_data.csv')
print(df_test.head())

# Adăugăm coloane noi în setul de date de test pentru fiecare subtask
df_test['Subtask1'] = 0.0  # Subtask1 va avea un rezultat de tip float
df_test['Subtask2'] = False  # Subtask2 va avea un rezultat de tip boolean
df_test['Subtask3'] = 0  # Subtask3 va avea un rezultat de tip întreg
df_test['Subtask4'] = 0  # Subtask4 va avea un rezultat de tip întreg
df_test['Subtask5'] = 0.0  # Subtask5 va avea un rezultat de tip float (aici vom adăuga predicțiile)

# Inițializăm o listă goală pentru a stoca rezultatele
result = []

# Iterăm prin fiecare rând al setului de date de test
for _, row in df_test.iterrows():
    # Iterăm prin subtasks (Subtask1 până la Subtask5)
    for subtask_id in range(1, 6):
        # Adăugăm un dicționar cu valorile corespunzătoare fiecărui subtask
        result.append({
            'subtaskID': subtask_id,  # ID-ul subtask-ului
            'datapointID': row['ID'],  # ID-ul datapoint-ului din rândul curent
            'answer': row[f'Subtask{subtask_id}']  # Răspunsul pentru subtask-ul curent
        })

# Creăm un DataFrame cu rezultatele obținute
df_output = pd.DataFrame(result)

# Afișăm primele 5 rânduri din DataFrame-ul rezultat
df_output.head()

# Salvăm rezultatele într-un fișier CSV pe care să-l putem apoi submite pe platformă
df_output.to_csv('submission.csv', index=False)
