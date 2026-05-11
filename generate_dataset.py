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

orientation_profiles = {
    'Médecine': {
        'filiere_bac': ['SVT', 'PC'],
        'notes': {
            'note_maths': (14.7, 1.2),
            'note_sciences': (17.2, 1.0),
            'note_physique': (15.8, 1.1),
            'note_langues': (12.4, 1.3),
            'note_philo': (11.4, 1.4),
        },
        'interets': ['Biologie', 'Santé', 'Sciences'],
    },
    'Informatique': {
        'filiere_bac': ['PC', 'STM', 'SVT'],
        'notes': {
            'note_maths': (17.0, 1.0),
            'note_sciences': (13.0, 1.3),
            'note_physique': (13.8, 1.2),
            'note_langues': (10.8, 1.2),
            'note_philo': (10.3, 1.3),
        },
        'interets': ['Technologie', 'Programmation', 'Jeux vidéo'],
    },
    'Ingénierie': {
        'filiere_bac': ['PC', 'STM', 'SVT'],
        'notes': {
            'note_maths': (15.4, 1.1),
            'note_sciences': (13.2, 1.3),
            'note_physique': (16.8, 1.0),
            'note_langues': (10.6, 1.2),
            'note_philo': (10.3, 1.3),
        },
        'interets': ['Technologie', 'Mécanique', 'Construction'],
    },
    'Commerce': {
        'filiere_bac': ['Economie', 'Lettres', 'PC'],
        'notes': {
            'note_maths': (12.2, 1.3),
            'note_sciences': (9.4, 1.3),
            'note_physique': (9.3, 1.3),
            'note_langues': (15.0, 1.1),
            'note_philo': (12.4, 1.2),
        },
        'interets': ['Business', 'Finance', 'Marketing'],
    },
    'Droit': {
        'filiere_bac': ['Lettres', 'Economie', 'SVT'],
        'notes': {
            'note_maths': (9.2, 1.2),
            'note_sciences': (9.2, 1.2),
            'note_physique': (8.8, 1.2),
            'note_langues': (15.5, 1.0),
            'note_philo': (16.8, 0.9),
        },
        'interets': ['Justice', 'Politique', 'Histoire'],
    },
    'Architecture': {
        'filiere_bac': ['STM', 'PC', 'SVT'],
        'notes': {
            'note_maths': (13.6, 1.2),
            'note_sciences': (12.0, 1.3),
            'note_physique': (13.6, 1.1),
            'note_langues': (12.0, 1.2),
            'note_philo': (11.8, 1.2),
        },
        'interets': ['Art', 'Construction', 'Design'],
    },
    'Langues': {
        'filiere_bac': ['Lettres', 'Economie', 'SVT'],
        'notes': {
            'note_maths': (8.8, 1.2),
            'note_sciences': (8.8, 1.2),
            'note_physique': (8.6, 1.1),
            'note_langues': (17.4, 0.9),
            'note_philo': (13.8, 1.1),
        },
        'interets': ['Littérature', 'Voyage', 'Culture'],
    },
    'Psychologie': {
        'filiere_bac': ['SVT', 'Lettres', 'Economie'],
        'notes': {
            'note_maths': (9.0, 1.2),
            'note_sciences': (13.3, 1.1),
            'note_physique': (9.0, 1.1),
            'note_langues': (13.5, 1.1),
            'note_philo': (15.8, 0.9),
        },
        'interets': ['Sciences humaines', 'Santé', 'Philosophie'],
    },
}


def sample_note(mean, std):
    value = np.random.normal(mean, std)
    return round(float(np.clip(value, 0, 20)), 1)


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


def adjust_note(value, delta_min, delta_max, sign):
    delta = np.random.uniform(delta_min, delta_max) * sign
    return round(float(np.clip(value + delta, 0, 20)), 1)


def generate_profile(orientation):
    config = orientation_profiles[orientation]
    profile = {}

    preferred_filieres = config['filiere_bac']
    if random.random() < 0.94:
        profile['filiere_bac'] = random.choice(preferred_filieres)
    else:
        profile['filiere_bac'] = random.choice(filieres_bac)

    for subject, (mean, std) in config['notes'].items():
        profile[subject] = sample_note(mean, std)

    interests = config['interets']
    all_interests = [
        'Technologie', 'Programmation', 'Jeux vidéo', 'Biologie', 'Santé',
        'Sciences', 'Business', 'Finance', 'Marketing', 'Mécanique',
        'Construction', 'Justice', 'Politique', 'Histoire', 'Art', 'Design',
        'Littérature', 'Voyage', 'Culture', 'Sciences humaines', 'Philosophie'
    ]
    if random.random() < 0.92:
        profile['interet_principal'] = random.choice(interests)
    else:
        profile['interet_principal'] = random.choice(all_interests)

    profile['niveau'] = weighted_choice(['Lycée', 'Université'], [3, 2])

    # Small irregularities keep the data realistic without making labels random.
    subjects = ['note_maths', 'note_sciences', 'note_physique', 'note_langues', 'note_philo']
    if random.random() < 0.03:
        subject = random.choice(subjects)
        profile[subject] = adjust_note(profile[subject], 1.5, 3.0, -1)

    if random.random() < 0.02:
        subject = random.choice(subjects)
        profile[subject] = adjust_note(profile[subject], 1.0, 2.5, 1)

    profile['orientation'] = orientation
    return profile


data = []
per_orientation = 2000 // len(orientations)

for orientation in orientations:
    for _ in range(per_orientation):
        data.append(generate_profile(orientation))

df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('moroccan_students.csv', index=False)
print('Dataset généré !')
print(df.head())
print('\nRépartition:')
print(df['orientation'].value_counts())
print('\nMoyennes par orientation:')
print(df.groupby('orientation')[['note_maths', 'note_sciences', 'note_physique', 'note_langues', 'note_philo']].mean().round(1))
