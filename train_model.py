import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv('moroccan_students.csv')

print("Colonnes:", df.columns.tolist())
print("Taille:", df.shape)

# Encoder les colonnes textuelles
le_dict = {}
for col in df.select_dtypes(include='object').columns:
    if col != 'orientation':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

X = df.drop('orientation', axis=1)
y = df['orientation']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"\nPrécision : {acc*100:.1f}%")
print("\nRapport détaillé:")
print(classification_report(y_test, pred))

joblib.dump(model, 'model.pkl')
joblib.dump(list(X.columns), 'columns.pkl')
joblib.dump(le_dict, 'encoders.pkl')
print("\nModèle sauvegardé !")