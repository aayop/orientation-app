# orientation-app

Application web Flask d'orientation académique basée sur un modèle de classification entraîné sur des profils d'étudiants.

## Prérequis

- Python 3.10+
- Un environnement virtuel Python

## Installation

Depuis `C:\Users\yousr\Desktop\git\orientation-app` :

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si le dossier `.venv` n'existe pas :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Lancer l'application

```powershell
.\.venv\Scripts\python.exe app.py
```

Ensuite ouvrir :

```text
http://127.0.0.1:5000
```

## Fonctionnement

L'application :

- charge `model.pkl`, `columns.pkl` et `encoders.pkl` au démarrage ;
- affiche un formulaire web pour saisir le profil étudiant ;
- envoie les données à la route `/predict` ;
- retourne une orientation recommandée.

## Réentraîner le modèle

Si vous voulez régénérer les données puis réentraîner le modèle :

```powershell
.\.venv\Scripts\python.exe generate_dataset.py
.\.venv\Scripts\python.exe train_model.py
```

## Dépendances importantes

Le projet a besoin au minimum de :

- Flask
- pandas
- scikit-learn
- joblib

## Problèmes fréquents

### `ModuleNotFoundError: No module named 'flask'`

Installer les dépendances :

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Le serveur démarre mais la page ne s'affiche pas

Vérifier que vous ouvrez bien :

```text
http://127.0.0.1:5000
```

### Le modèle ne se charge pas

Vérifier que ces fichiers existent dans le dossier du projet :

- `model.pkl`
- `columns.pkl`
- `encoders.pkl`
