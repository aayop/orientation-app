import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv('moroccan_students.csv')

print("Colonnes:", df.columns.tolist())
print("Taille:", df.shape)

X = df.drop('orientation', axis=1)
y = df['orientation']
categorical_cols = X.select_dtypes(include='object').columns.tolist()
numeric_cols = [col for col in X.columns if col not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ('numeric', 'passthrough', numeric_cols),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Pipeline(
    steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight='balanced',
        )),
    ]
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"\nPrécision : {acc*100:.1f}%")
print("\nRapport détaillé:")
print(classification_report(y_test, pred))

joblib.dump(model, 'model.pkl')
joblib.dump(list(X.columns), 'columns.pkl')
joblib.dump({}, 'encoders.pkl')
print("\nModèle sauvegardé !")
