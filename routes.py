from flask import render_template, request
import pickle
from . import project2_bp

with open(r'C:\Users\Dell User\Desktop\Flask-Blueprints\models\food_recommendation_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open(r'C:\Users\Dell User\Desktop\Flask-Blueprints\models\label_encoders.pkl', 'rb') as encoders_file:
    label_encoder_country, label_encoder_weather, label_encoder_food_type, mlb = pickle.load(encoders_file)


countries = ['USA', 'Italy', 'India', 'Japan']
weathers = ['Sunny', 'Rainy', 'Moderate', 'Cold']
food_types = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']

@project2_bp.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    
    if request.method == 'POST':

        country = request.form.get('country')
        weather = request.form.get('weather')
        food_type = request.form.get('food_type')

        encoded_country = label_encoder_country.transform([country])[0]
        encoded_weather = label_encoder_weather.transform([weather])[0]
        encoded_food_type = label_encoder_food_type.transform([food_type])[0]
        

        input_features = [[encoded_country, encoded_weather, encoded_food_type]]

        predicted_labels = model.predict(input_features)
        recommendations = mlb.inverse_transform(predicted_labels)[0]
    
    return render_template('index.html', recommendations=recommendations, countries=countries, weathers=weathers, food_types=food_types)
