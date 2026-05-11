from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import unicodedata

app = Flask(__name__)

model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')
le_dict = joblib.load('encoders.pkl')
categorical_cols = ['filiere_bac', 'interet_principal', 'niveau']


def _fix_mojibake(value):
    if not isinstance(value, str):
        return value

    value = value.strip()
    try:
        repaired = value.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        repaired = value
    return repaired.strip()


def _normalize_label(value):
    value = _fix_mojibake(value)
    if not isinstance(value, str):
        return value
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(char for char in value if not unicodedata.combining(char))
    return value.lower().strip()


def _get_pipeline_category_maps():
    if not hasattr(model, 'named_steps') or 'preprocessor' not in model.named_steps:
        return {}

    preprocessor = model.named_steps['preprocessor']
    transformer = preprocessor.named_transformers_.get('categorical')
    if transformer is None:
        return {}

    return {
        col: {_normalize_label(category): category for category in categories}
        for col, categories in zip(categorical_cols, transformer.categories_)
    }


def _get_model_classes():
    if hasattr(model, 'classes_'):
        return model.classes_
    if hasattr(model, 'named_steps') and 'classifier' in model.named_steps:
        return model.named_steps['classifier'].classes_
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    numeric_cols = ['note_maths', 'note_sciences', 'note_physique', 
                    'note_langues', 'note_philo']

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    notes = df[numeric_cols].iloc[0]
    if notes.mean() < 10 or (notes < 8).sum() >= 4:
        return jsonify({'orientation': 'Profil à renforcer'})

    category_maps = _get_pipeline_category_maps()
    for col, class_map in category_maps.items():
        if col in df.columns:
            df[col] = df[col].map(lambda value: class_map.get(_normalize_label(value), value))
            unknown = sorted(set(df[col]) - set(class_map.values()))
            if unknown:
                return jsonify({
                    'error': f"Valeur non reconnue pour '{col}': {unknown[0]}"
                }), 400

    for col, le in le_dict.items():
        if col in df.columns:
            class_map = {_normalize_label(label): label for label in le.classes_}
            df[col] = df[col].map(lambda value: class_map.get(_normalize_label(value), value))
            unknown = sorted(set(df[col]) - set(le.classes_))
            if unknown:
                return jsonify({
                    'error': f"Valeur non reconnue pour '{col}': {unknown[0]}"
                }), 400
            df[col] = le.transform(df[col])

    df = df[columns]
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    top_predictions = sorted(
        [
            {
                'orientation': orientation,
                'probability': round(float(probability) * 100, 1)
            }
            for orientation, probability in zip(_get_model_classes(), probabilities)
        ],
        key=lambda item: item['probability'],
        reverse=True
    )
    top_probability = top_predictions[0]['probability'] if top_predictions else 0
    second_probability = top_predictions[1]['probability'] if len(top_predictions) > 1 else 0

    if top_probability < 45 or (top_probability < 65 and top_probability - second_probability < 12):
        return jsonify({
            'orientation': 'Profil ambigu',
            'probabilities': top_predictions
        })

    return jsonify({
        'orientation': prediction,
        'probabilities': top_predictions
    })

if __name__ == '__main__':
    app.run(debug=True)
