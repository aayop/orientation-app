import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('cs_students.csv')

# Supprimer les colonnes inutiles
df = df.drop(['Student ID', 'Name'], axis=1)

# Encoder toutes les colonnes textuelles
le_dict = {}
for col in df.select_dtypes(include='object').columns:
    if col != 'Future Career':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

X = df.drop('Future Career', axis=1)
y = df['Future Career']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"Précision : {acc*100:.1f}%")
print("Colonnes utilisées:", X.columns.tolist())

joblib.dump(model, 'model.pkl')
joblib.dump(list(X.columns), 'columns.pkl')
joblib.dump(le_dict, 'encoders.pkl')
print("Modèle sauvegardé !")