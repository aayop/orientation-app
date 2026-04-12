from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')
le_dict = joblib.load('encoders.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])

    for col, le in le_dict.items():
        if col in df.columns:
            df[col] = le.transform(df[col])

    numeric_cols = ['note_maths', 'note_sciences', 'note_physique', 
                    'note_langues', 'note_philo']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df = df[columns]
    prediction = model.predict(df)[0]
    return jsonify({'orientation': prediction})

if __name__ == '__main__':
    app.run(debug=True)