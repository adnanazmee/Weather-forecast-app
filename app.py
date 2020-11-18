import requests
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'

db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)



@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_location = request.form.get('city')

        if new_location:
            new_location_obj = Location(name=new_location)

            db.session.add(new_location_obj)
            db.session.commit()

    cities = Location.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'country': r['sys']['country'],
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

