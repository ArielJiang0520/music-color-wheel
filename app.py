# app.py
from flask import Flask, request, jsonify
from flask import render_template
import toolfunc as tools
import json

import pickle
import pandas

color_df = pickle.load(open("color_df.p", "rb"))

app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/closest', methods=['GET'])
def closest():
    color = request.args['color']
    color = json.loads(color)
    closest = tools.getClosestSong(color['r'], color['g'], color['b'], color_df)
    closest['popularity'] = int(closest['popularity'])
    closest['R'] = int(closest['R'])
    closest['G'] = int(closest['G'])

    closest['B'] = int(closest['B'])

    print(closest)

    # closest = json.dumps(closest)    # print(request.args['color'])
    return jsonify({"results":closest})

@app.route('/genre', methods=['GET'])
def genre():
    # genre = request.args['genre']
    topN = tools.getGenreTopN('british soul', color_df, 10)
    print(topN)
    return jsonify({"results":topN})

@app.route('/artist', methods=['GET'])
def artist():
    artist =  tools.getArtistColor('Adele', color_df)
    print(artist)
    # artist[0] = int(artist[0])
    # artist[1] = int(artist[1])
    # artist[2] = int(artist[2])

    return jsonify({"results":artist})



@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)