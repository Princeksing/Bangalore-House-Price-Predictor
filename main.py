from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)


# -----------------------------------------
# Load Cleaned Dataset
# -----------------------------------------

data = pd.read_csv("Cleaned_data.csv")


# -----------------------------------------
# Load Trained Ridge Regression Model
# -----------------------------------------

with open("RidgeModel.pkl", "rb") as file:
    model = pickle.load(file)


# -----------------------------------------
# Home Page
# -----------------------------------------

@app.route('/')
def index():

    # Get all unique locations
    locations = sorted(data['location'].dropna().unique())

    return render_template(
        'index.html',
        locations=locations,
        prediction=None,
        selected_location=None,
        bhk=None,
        bath=None,
        total_sqft=None
    )


# -----------------------------------------
# Prediction Route
# -----------------------------------------

@app.route('/predict', methods=['POST'])
def predict():

    try:
        # Get values entered by user
        location = request.form.get('location')
        bhk = float(request.form.get('bhk'))
        bath = float(request.form.get('bath'))
        total_sqft = float(request.form.get('total_sqft'))


        # Create dataframe for prediction
        # Column order must match model training data
        input_data = pd.DataFrame(
            [[location, total_sqft, bath, bhk]],
            columns=[
                'location',
                'total_sqft',
                'bath',
                'bhk'
            ]
        )


        # Predict house price
        prediction = model.predict(input_data)[0]


        # Get locations again for dropdown
        locations = sorted(
            data['location'].dropna().unique()
        )


        # Return prediction to HTML
        return render_template(
            'index.html',

            locations=locations,

            prediction=round(float(prediction), 2),

            # Keep entered values after prediction
            selected_location=location,
            bhk=bhk,
            bath=bath,
            total_sqft=total_sqft
        )


    except Exception as e:

        return f"Prediction Error: {str(e)}"


# -----------------------------------------
# Run Flask Application
# -----------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )