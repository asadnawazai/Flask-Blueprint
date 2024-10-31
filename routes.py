from flask import render_template, request, jsonify
import joblib
import pandas as pd
from . import project1_bp
from utils_p1 import food


column_transformer = joblib.load(r'C:\Users\Dell User\Desktop\Flask-Blueprints\models\column_transformer.pkl')
model = joblib.load(r'C:\Users\Dell User\Desktop\Flask-Blueprints\models\wine_recommendation_model.pkl')

dishes = ['Grilled Steak', 'Spaghetti Carbonara', 'Caesar Salad', 'Roasted Salmon', 'Chicken Alfredo', 'Margherita Pizza', 'Shrimp Tacos', 'Dark Chocolate Cake']
ingredients = ['Beef, Salt, Pepper, Garlic', 'Pasta, Egg, Bacon, Parmesan', 'Romaine, Croutons, Parmesan, Anchovy', 'Salmon, Lemon, Dill, Olive Oil', 'Chicken, Cream, Butter, Parmesan', 'Tomato, Mozzarella, Basil', 'Shrimp, Lime, Cilantro, Avocado', 'Cocoa, Sugar, Butter']
cooking_styles = ['Grilled', 'Boiled', 'Fresh', 'Roasted', 'Creamy', 'Baked', 'Grilled', 'Baked']
flavors = ['Savory, Umami', 'Creamy, Salty', 'Salty, Tangy', 'Citrusy, Savory', 'Rich, Savory', 'Savory, Herby', 'Spicy, Citrusy', 'Sweet, Rich']
textures = ['Tender', 'Creamy', 'Crunchy', 'Flaky', 'Creamy', 'Crispy', 'Crunchy', 'Dense']

@project1_bp.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        input_data = pd.DataFrame({
            'Dish Name': [request.form.get('dish_name')],
            'Ingredients': [request.form.get('ingredients')],
            'Cooking Style': [request.form.get('cooking_style')],
            'Flavors': [request.form.get('flavors')],
            'Texture': [request.form.get('texture')]
        })
        transformed_input = column_transformer.transform(input_data)
        prediction = model.predict(transformed_input)[0]

    return render_template('form.html', prediction=prediction, dishes=dishes, 
                           ingredients=ingredients, cooking_styles=cooking_styles,
                           flavors=flavors, textures=textures)

@project1_bp.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.json
    required_fields = ['dish_name', 'ingredients', 'cooking_style', 'flavors', 'texture']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields in request'}), 400

    input_data = pd.DataFrame({
        'Dish Name': [data['dish_name']],
        'Ingredients': [data['ingredients']],
        'Cooking Style': [data['cooking_style']],
        'Flavors': [data['flavors']],
        'Texture': [data['texture']]
    })
    transformed_input = column_transformer.transform(input_data)
    prediction = model.predict(transformed_input)[0]

    return jsonify({'prediction': prediction})
