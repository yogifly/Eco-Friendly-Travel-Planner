from flask import Flask, render_template, request, redirect, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "edupro-614e5",
  "private_key_id": "24bed4bacabd11d5d542ba54250bde583f3513a3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+0/l3LZY2c9D5\nM4/tdFgGpIhuv1YSN/RBzPz9YclT6mNZZ9csgkdkL84UC+waL/Cs2k6zMykTgeu+\nMMlTLBTPlQKugB0tysHRlH6AO6vFvC/M9FZ2eDJhKQv4zd6dqVMcskDi+nYFhKhK\n/sdeIuJs8diXfkhIn2mvTjZfGRmJBrTWA/cX17SYM309e9ffbq6xD6a04whXOgkK\nwfRrxWpAevqHnMVTOY5MfbQDVHdHf/9A/aNlygEmnRiMXMvAOLLEkSfNp5kSYZp4\nAndy++N6SFs8tKohdPExbvH1gka0BIJAuAa07Okc2FptWZPnjNFaAB0NMB30vnBb\nlIbtW9PJAgMBAAECggEAAfNs03kV1gytED8ks4rC855u/qLaIGmOB7Yux/Bd/Iui\n5GEZZA0Y6b9LXg0ZJtNipIG+2Donq1lirZkWFdGXjN+7HUmWAsfV32yjNnBluynH\nW1MMJz3nVfLzemGwavA2N07jNu7Ukg3fIpUkOKQmqHJ4gmP6HTP0AqTMDYDWL/5r\nAmDpx+IElfm51aqcrU2IgWjw7GaJcn1isXYDcC2JoOvNI24cbrwxgh+I77xR+eWj\nlHvP1f2/GhhpNF+GCIunPQpAWWWVOiusqj3kFMrfdlKFe+FtUhZ2fciDXqcGX7qu\ns3rMoz/kIzyc/v53UFM48bUgzWxmWeuYqvomydQOAQKBgQD3xlnQkrFXIOSMnH7W\n3zMkKdlJe7N8SBklL73tIrTnlYN1sOzKaSIILgqrGSt6M4kYjet+ZqTrE2S9rbyf\nm3pjvBIrqf4HxG4ynsT4k7jsdUuC35dNjik/kWdHOpj/vVry9YiyW41O77Oicgec\niZls/77C41CcoVowVJbO8pnMKQKBgQDFKa0lc6aRbsiEWPwbx5pfX6+9wvG07rb7\nOL1hYqx6Fit12URIiZDvdGcq0TnpIFaflYAQcGcm8ovq//ipcUfxidZVrsTW8GBd\nLp2opA4jpjxYl5vBoeXWNjB99l3N72GP/vU0/8Mt/wF6O7d8CChmSi4NiO+jl2xu\nbFBW77y+oQKBgCGtqE+dYNWC9w3Vx7fVJtJnjc1bLw5ZjnFrh9lPul8wB2pb3hO1\nLpcGCxUumqZFkwDvaW8I7Km3PR47G0RmkcA0tBOTS6Aqpv/ibMuM6LnbR6RGV/6G\nsDyfuvYHlPxN9KrJjQcRQqfUFQqjjT1Nxrj2GivLUg24MNYY6Va/yv/hAoGAHx58\n3bRrTfkWXQ1OfXP7waHwsxrZ25zx9KT3/y772ik1otwwEuLjpWfSAMgVQ95+zaFj\nHTUgkt0liGnubZAbstv2oH99Qg+ephZ9e+io8qeCTtlfFCjhhfX3oWoJVD+8PmYX\nfc4AmHnvWcOjKkh/V+XNbwV2DXQRATzHUXF1cQECgYBG21Ck/8LiE38BXJpjR8rC\nk3auxzO+TGjglGdI23McaWMSn5S42ILGyvJLjHfTRRkMgVYZH7WF05UpzX0lo7FO\noKUZJThw+jXcmaSxK6SC6gyZNEn4fwohPqHvwBPjGBIo/Ua1kbR9+MvqS1NyZLjB\nr7OyMgvQLh6ZH+SiK+Ay5A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2xdvk@edupro-614e5.iam.gserviceaccount.com",
  "client_id": "112298848561670180112",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2xdvk%40edupro-614e5.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
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
            
            return redirect(url_for('features'))
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




if __name__ == '__main__':
    app.run(debug=True)
