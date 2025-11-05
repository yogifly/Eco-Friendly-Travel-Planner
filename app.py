from flask import Flask, render_template, request, redirect, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate({
"Google Cloud Credentials"
})

firebase_admin.initialize_app(cred)


app = Flask(__name__)

# Function to calculate carbon footprint
def calculate_carbon_footprint(distance, transport_mode):
    emission_rates = {
        'flight': 0.255,     # kg CO2 per km for flight
        'train': 0.041,      # kg CO2 per km for train
        'car': 0.192,        # kg CO2 per km for car
        'bus': 0.105,        # kg CO2 per km for bus
        'bike': 0.000,       # kg CO2 per km for bike (no emissions)
        'electric_car': 0.051  # kg CO2 per km for electric car
    }

    greener_alternatives = {
        'flight': "Train or Bus",
        'train': "Bike or Electric Car",
        'car': "Bus or Bike",
        'bus': "Bike or Electric Car",
        'bike': "No greener alternative needed (you're already eco-friendly!)",
        'electric_car': "Bike or Train"
    }

    def carbon_offset_options(carbon_footprint):
        return {
            "tree_planting": round(carbon_footprint / 0.0025),  # Number of trees to plant
            "renewable_energy": round(carbon_footprint / 0.01), # Amount of energy in MWh
            "carbon_credits": round(carbon_footprint / 0.5)     # Carbon credits needed
        }

    carbon_footprint = distance * emission_rates.get(transport_mode, 0)
    greener_alternative = greener_alternatives.get(transport_mode, "No alternative available")
    carbon_offset = carbon_offset_options(carbon_footprint)

    return {
        "carbonFootprint": carbon_footprint,
        "greenerAlternative": greener_alternative,
        "carbonOffset": carbon_offset
    }

# Route to serve the carbon footprint HTML page
@app.route('/carbon')
def carbon():
    return render_template('carbon.html')

# POST route to calculate carbon footprint
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    distance = data.get('distance')
    transport_mode = data.get('transportMode')

    result = calculate_carbon_footprint(distance, transport_mode)
    return jsonify(result)

# Route for login page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
         
            user = auth.create_user(
                email=email,
                password=password
            )
            
            return redirect(url_for('features'))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
          
            user = auth.get_user_by_email(email)
            
            return redirect(url_for('Home'))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return render_template('login.html')

# Route for features page
@app.route('/features')
def features():
    return render_template('features.html')



@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/')
def home():
    return render_template('head.html')

@app.route('/checklist')
def checklist():
    return render_template('checklist.html')

@app.route('/places')
def places():
    return render_template('places.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/local')
def local():
    return render_template('local.html')

@app.route('/activities1')
def activities1():
    return render_template('activities1.html')

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/vol')
def vol():
    return render_template('vol.html')

@app.route('/Home')
def Home():
    return render_template('Home.html')




if __name__ == '__main__':
    app.run(debug=True)
