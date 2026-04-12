import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

filieres_bac = ['SVT', 'PC', 'STM', 'Lettres', 'Economie']

orientations = [
    'Informatique', 'Médecine', 'Commerce', 'Ingénierie',
    'Droit', 'Architecture', 'Langues', 'Psychologie'
]

def generer_profil(orientation):
    profil = {}

    # Filière bac
    if orientation == 'Médecine':
        profil['filiere_bac'] = random.choice(['SVT', 'PC'])
        profil['note_maths'] = round(random.uniform(14, 20), 1)
        profil['note_sciences'] = round(random.uniform(16, 20), 1)
        profil['note_physique'] = round(random.uniform(14, 20), 1)
        profil['note_langues'] = round(random.uniform(12, 18), 1)
        profil['note_philo'] = round(random.uniform(10, 16), 1)
    elif orientation == 'Informatique':
        profil['filiere_bac'] = random.choice(['PC', 'STM'])
        profil['note_maths'] = round(random.uniform(15, 20), 1)
        profil['note_sciences'] = round(random.uniform(12, 18), 1)
        profil['note_physique'] = round(random.uniform(14, 20), 1)
        profil['note_langues'] = round(random.uniform(12, 17), 1)
        profil['note_philo'] = round(random.uniform(10, 15), 1)
    elif orientation == 'Ingénierie':
        profil['filiere_bac'] = random.choice(['PC', 'STM'])
        profil['note_maths'] = round(random.uniform(14, 20), 1)
        profil['note_sciences'] = round(random.uniform(13, 19), 1)
        profil['note_physique'] = round(random.uniform(15, 20), 1)
        profil['note_langues'] = round(random.uniform(11, 16), 1)
        profil['note_philo'] = round(random.uniform(10, 15), 1)
    elif orientation == 'Commerce':
        profil['filiere_bac'] = random.choice(['Economie', 'Lettres'])
        profil['note_maths'] = round(random.uniform(12, 18), 1)
        profil['note_sciences'] = round(random.uniform(10, 15), 1)
        profil['note_physique'] = round(random.uniform(10, 15), 1)
        profil['note_langues'] = round(random.uniform(14, 20), 1)
        profil['note_philo'] = round(random.uniform(12, 17), 1)
    elif orientation == 'Droit':
        profil['filiere_bac'] = random.choice(['Lettres', 'Economie'])
        profil['note_maths'] = round(random.uniform(10, 16), 1)
        profil['note_sciences'] = round(random.uniform(10, 14), 1)
        profil['note_physique'] = round(random.uniform(10, 14), 1)
        profil['note_langues'] = round(random.uniform(15, 20), 1)
        profil['note_philo'] = round(random.uniform(15, 20), 1)
    elif orientation == 'Architecture':
        profil['filiere_bac'] = random.choice(['STM', 'PC'])
        profil['note_maths'] = round(random.uniform(13, 19), 1)
        profil['note_sciences'] = round(random.uniform(12, 17), 1)
        profil['note_physique'] = round(random.uniform(13, 18), 1)
        profil['note_langues'] = round(random.uniform(12, 17), 1)
        profil['note_philo'] = round(random.uniform(11, 16), 1)
    elif orientation == 'Langues':
        profil['filiere_bac'] = random.choice(['Lettres', 'Economie'])
        profil['note_maths'] = round(random.uniform(10, 15), 1)
        profil['note_sciences'] = round(random.uniform(10, 14), 1)
        profil['note_physique'] = round(random.uniform(10, 14), 1)
        profil['note_langues'] = round(random.uniform(16, 20), 1)
        profil['note_philo'] = round(random.uniform(13, 18), 1)
    elif orientation == 'Psychologie':
        profil['filiere_bac'] = random.choice(['SVT', 'Lettres'])
        profil['note_maths'] = round(random.uniform(10, 15), 1)
        profil['note_sciences'] = round(random.uniform(12, 17), 1)
        profil['note_physique'] = round(random.uniform(10, 15), 1)
        profil['note_langues'] = round(random.uniform(13, 18), 1)
        profil['note_philo'] = round(random.uniform(14, 20), 1)

    # Intérêts
    interets_map = {
        'Informatique': ['Technologie', 'Programmation', 'Jeux vidéo'],
        'Médecine': ['Biologie', 'Santé', 'Sciences'],
        'Commerce': ['Business', 'Finance', 'Marketing'],
        'Ingénierie': ['Technologie', 'Mécanique', 'Construction'],
        'Droit': ['Justice', 'Politique', 'Histoire'],
        'Architecture': ['Art', 'Construction', 'Design'],
        'Langues': ['Littérature', 'Voyage', 'Culture'],
        'Psychologie': ['Sciences humaines', 'Santé', 'Philosophie']
    }
    profil['interet_principal'] = random.choice(interets_map[orientation])

    # Niveau
    profil['niveau'] = random.choice(['Lycée', 'Université'])

    # Orientation
    profil['orientation'] = orientation

    return profil

# Générer 2000 lignes
data = []
par_orientation = 2000 // len(orientations)

for orientation in orientations:
    for _ in range(par_orientation):
        data.append(generer_profil(orientation))

df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('moroccan_students.csv', index=False)
print("Dataset généré !")
print(df.head())
print("\nRépartition:")
print(df['orientation'].value_counts())