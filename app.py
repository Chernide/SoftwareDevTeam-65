from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import requests
import os
import json
import bcrypt
import psycopg2
import binascii

# Returns a list of dictionaries for each politician
# This can then be converted to JSON
def processCivicResp(response):
    info = json.loads(response)
    offices = info['offices']
    officials = info['officials']
    retInfo = []
    for office in offices:
        for i in office['officialIndices']:
            official = officials[i]
            politician = {}
            # Add the politician's office (like "United States Senator") to their entry
            politician['officeName'] = office['name']
            # Full keys are 'address', 'name', 'party', 'photoUrl', 'channels', 'urls', 'phones', emails
            # Some officials don't have a website or a photoUrl though
            # I was planning on copying over all of those keys anyway so this works
            for key in official.keys():
                politician[key] = official[key]
        retInfo.append(politician)

    return retInfo


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ['JWT_KEY']
jwt = JWTManager(app)

@app.route('/')
def index():
    return "This probably isn't what you want.\n Try /getPoliticians/YOUR_ZIP for a list of your local politicians"

@app.route('/signup', methods=['get', 'post'])
def signup():
    content = request.get_json(silent = True)
    email = content.get('email')
    password = content.get('password')

    if email == None or password == None:
        return jsonify({'msg': 'Email/password not provided'}), 400
    else:
        conn = psycopg2.connect( host=os.environ['HostName'], user=os.environ['UserName'], password=os.environ['password'], dbname=os.environ['DataBase'], port="5432")
        cur = conn.cursor()
        command = "SELECT * FROM users WHERE email = (%s);"
        data = (email, )
        cur.execute(command, data)
        result = cur.fetchall()

        if len(result) > 0:
            cur.close()
            conn.close()
            return jsonify({'msg': 'Account already taken'}), 401
        else:
            encPwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            encPwd = encPwd.decode('utf-8') # weird conversion from bytes to string to make SQL play nice
            createAccount = "INSERT INTO users (email, encrypted_Password) VALUES (%s, %s)"
            accountData = (email, encPwd)
            cur.execute(createAccount, accountData)
            conn.commit()

            cur.close()
            conn.close()
            token = create_access_token(email)
            return jsonify({'token': token}), 200


@app.route('/login', methods=['get', 'post'])
def login():
    content = request.get_json(silent = True)
    email = content.get('email')
    password = content.get('password')
    msg = "Not enough information"

    if email == None or password == None:
        return jsonify({'msg': 'Email/password not provided'}), 400
    else:
        conn = psycopg2.connect( host=os.environ['HostName'], user=os.environ['UserName'], password=os.environ['password'], dbname=os.environ['DataBase'], port="5432")
        cur = conn.cursor()
        command = "SELECT * FROM users WHERE email = (%s);"
        data = (email, )
        cur.execute(command, data)
        result = cur.fetchall()
        cur.close()
        conn.close()

        if len(result) > 0:
            print(result[0])
            hashedPw = result[0][2]
            correctPw = bcrypt.checkpw(password.encode('utf-8'), hashedPw.encode('utf-8'))
            if correctPw:
                token = create_access_token(email)
                return jsonify({'token': token}), 200
            else:
                return jsonify({'msg': 'Invalid credentials'}), 401
        else:
            return jsonify({'msg': 'User not found'}), 404

# The route to an API response
# I can add more arguments to the url like a password later
@app.route('/getPoliticians')
@jwt_required
def getPoliticians():
    city = request.args.get('city')
    state = request.args.get('state')
    city = city.strip()
    address = city + ', ' + state
    requestParams = {'key': os.environ["GoogleAPIKey"], 'address': address}
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives", params=requestParams)

    if info.status_code == 200:
        # The processed response puts all of the fields in alphabetical order because python is weird
        # Should be processed alright by the front end though
        return jsonify(processCivicResp(info.text))
    else:
        # If there is an error, return the error that google sends
        return info.text

# Returns the unprocessed response from the google API
# indenting for this is weird in a browser but alright in curl
@app.route('/civicInfo')
@jwt_required
def echoArgs():
    city = request.args.get('city')
    state = request.args.get('state')
    city = city.strip()
    address = city + ', ' + state
    requestParams = {'key': os.environ["GoogleAPIKey"], 'address': address}
    apiKey = os.environ["GoogleAPIKey"]
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives", params=requestParams)
    return info.text;

if __name__ == "__main__":
	app.run()
