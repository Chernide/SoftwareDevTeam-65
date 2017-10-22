from flask import Flask, jsonify, request
import requests
import os
import json

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
            # I was planning on copying over all of those keys anyway so this works ¯\_(ツ)_/¯
            for key in official.keys():
                politician[key] = official[key]
        retInfo.append(politician)

    return retInfo

app = Flask(__name__)

@app.route('/')
def index():
    return "This probably isn't what you want.\n Try /getPoliticians/YOUR_ZIP for a list of your local politicians"

# The route to an API response
# I can add more arguments to the url like a password later
@app.route('/getPoliticians/<int:zipCode>')
def getPoliticians(zipCode):
    # NOTE: The API can take state codes or even full addresses, but zip code is most efficient
    apiKey = os.environ["GoogleAPIKey"]
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives?key=%s&address=%d" % (apiKey, zipCode))

    if info.status_code == 200:
        # The processed response puts all of the fields in alphabetical order because python is weird
        # Should be processed alright by the front end though
        return jsonify(processCivicResp(info.text))
    else:
        # If there is an error, return the error that google sends
        return info.text

# Returns the unprocessed response from the google API
# indenting for this is weird in a browser but alright in curl
@app.route('/civicInfo/<int:zipCode>')
def echoArgs(zipCode):
    apiKey = os.environ["GoogleAPIKey"]
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives?key=%s&address=%d" % (apiKey, zipCode))
    return info.text;

if __name__ == "__main__":
	app.run()
