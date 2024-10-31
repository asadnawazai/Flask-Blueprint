from flask import Flask
from project1 import project1_bp
from project2 import project2_bp

app = Flask(__name__)

app.register_blueprint(project1_bp, url_prefix='/')
app.register_blueprint(project2_bp, url_prefix='/food')

if __name__ == '__main__':
    app.run(debug=True)
