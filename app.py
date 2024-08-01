from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load and prepare the model
rawdata = pd.read_csv('content/diabetes.csv')
X = rawdata.drop(columns='Outcome', axis=1)
Y = rawdata['Outcome']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, stratify=Y, random_state=2)
classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, Y_train)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = [data['Pregnancies'], data['Glucose'], data['BloodPressure'], data['SkinThickness'],
                  data['Insulin'], data['BMI'], data['DiabetesPedigreeFunction'], data['Age']]
    input_data = np.asarray(input_data).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)
    prediction = classifier.predict(input_data_scaled)

    return jsonify({'prediction': 'diabetic' if prediction[0] == 1 else 'not diabetic'})

if __name__ == "__main__":
    app.run(debug=True)
