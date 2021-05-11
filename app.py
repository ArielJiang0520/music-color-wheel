# app.py
from flask import Flask, request, jsonify
from flask import render_template
# import toolfunc as tools
import json
from data import Dataset

import pickle
import pandas

color_df = pickle.load(open("color_df.p", "rb"))
DB = Dataset(color_df)

app = Flask(__name__, static_url_path='')


allGenreList = ["dark clubbing", "yacht rock", "rhythm and blues", "chicago hardcore", "chamber pop", "beach music", "speed metal", "arkansas hip hop", "irish pop", "spanish indie folk", "modern salsa", "new wave", "worship", "la indie", "psychedelic blues-rock", "spanish indie pop", "ottawa rap", "reggaeton flow", "cork indie", "jazz pop", "australian alternative rock", "hip pop", "canadian pop", "synthpop", "virginia hip hop", "indie electropop", "groove metal", "mod revival", "albuquerque indie", "new jersey hardcore", "experimental rock", "battle rap", "gospel", "talent show", "sunshine pop", "djent", "german pop", "small room", "okc indie", "uk contemporary r&b", "viral trap", "northern irish indie", "contemporary jazz", "eurodance", "east coast hip hop", "euphoric hardstyle", "modern blues", "olympia wa indie", "new orleans blues", "nu metal", "gangster rap", "folk", "alternative rock", "bronx hip hop", "dutch prog", "washington indie", "jazz guitar", "christian pop", "bristol indie", "welsh metal", "melbourne bounce international", "screamo", "post-teen pop", "jazz orchestra", "german punk rock", "sheffield indie", "psychedelic soul", "acoustic rock", "grunge", "deep disco house", "nederpop", "flute rock", "chillwave", "rock independant francais", "future rock", "german rock", "celtic", "motown", "salsa", "uk metalcore", "australian pop", "pop electronico", "political hip hop", "dancehall", "queens hip hop", "german metal", "chilean indie", "modern jazz trio", "canadian celtic", "swedish electropop", "progressive trance", "electro", "deep groove house", "chicago punk", "scottish new wave", "new jersey punk", "uk americana", "american folk revival", "new rave", "pop rap", "blues", "dutch pop", "orgcore", "oakland hip hop", "progressive electro house", "slap house", "nu-metalcore", "british invasion", "british power metal", "memphis soul", "dutch rock", "dirty south rap", "brostep", "fremantle indie", "dutch edm", "jacksonville indie", "new jersey rap", "chilean rock", "classic country pop", "turntablism", "canadian folk", "barbadian pop", "filter house", "modern folk rock", "memphis hip hop", "shimmer pop", "punk", "chicago drill", "glitch hop", "deathgrind", "latin arena pop", "lo-fi beats", "german indie rock", "funk", "blues rock", "antideutsche", "reggae fusion", "german hip hop", "electronica", "pop house", "a cappella", "piano rock", "french shoegaze", "japanese post-rock", "glam metal", "lo-fi", "vancouver punk", "canadian indie", "irish folk", "folk rock", "europop", "shiver pop", "symphonic metal", "minnesota hip hop", "post-grunge", "indie pop", "louisville underground", "art rock", "classic uk pop", "german indie", "ontario indie", "gothenburg metal", "hyperpop", "tape club", "disco house", "melodic dubstep", "melancholia", "trap", "christian indie", "german thrash metal", "modern bollywood", "latin hip hop", "post-punk", "swing", "boston rock", "contemporary post-bop", "boogie-woogie", "g-house", "hamburg indie", "livetronica", "jazztronica", "gbvfi", "country gospel", "austindie", "afrofuturism", "contemporary country", "quiet storm", "wrestling", "future bass", "progressive bluegrass", "japanese indie rock", "vapor soul", "belgian dance", "ninja", "canadian classical", "experimental", "australian electropop", "buffalo ny indie", "canadian soundtrack", "swedish melodic rock", "indie rock", "cosmic american", "brighton indie", "indie folk", "austrian pop", "noise rock", "pop r&b", "alternative metal", "parody", "vocal house", "rap rock", "alternative r&b", "cantautor", "alabama rap", "outsider", "rochester ny indie", "dutch indie", "essex indie", "children's music", "south carolina hip hop", "indie quebecois", "trip hop", "texas pop punk", "souldies", "merseybeat", "chicago blues", "kiwi rock", "idaho indie", "east coast reggae", "nu jazz", "uk dance", "idol", "australian underground hip hop", "metalcore", "denver indie", "duluth indie", "thrash metal", "panamanian pop", "easy listening", "desi hip hop", "anthem worship", "new jack swing", "canadian pop punk", "industrial", "chill lounge", "protopunk", "jazz trumpet", "new americana", "show tunes", "oakland indie", "deep gothic post-punk", "jazz", "riot grrrl", "ccm", "moombahton", "neo-progressive", "canadian latin", "alt z", "supergroup", "symphonic rock", "australian rock", "icelandic indie", "j-rock", "rap conscient", "pop quebecois", "power pop", "instrumental rock", "roots americana", "nu gaze", "gainesville indie", "new orleans rap", "cali rap", "soul", "electra", "contemporary vocal jazz", "french metal", "transpop", "swedish singer-songwriter", "twee pop", "intelligent dance music", "uk pop", "post-doom metal", "digital hardcore", "instrumental bluegrass", "japanese shoegaze", "australian hip hop", "southern rock", "scottish rock", "classic girl group", "escape room", "britpop", "art punk", "gauze pop", "post-disco", "alternative americana", "classic hardstyle", "new orleans indie", "pub rock", "jazz rock", "swedish pop", "atlanta indie", "pop edm", "banjo", "swedish hard rock", "boston hip hop", "big room", "bakersfield sound", "nintendocore", "crunk", "urban contemporary", "bluegrass gospel", "southern soul", "emo rap", "hard rock", "deep contemporary country", "melodic thrash", "traditional blues", "mexican pop", "christian punk", "shoegaze", "stomp pop", "sludge metal", "latin alternative", "aussietronica", "microhouse", "indie game soundtrack", "rebel blues", "nashville sound", "post-hardcore", "country dawn", "melodic rap", "disney", "math rock", "soft rock", "movie tunes", "noise pop", "technical groove metal", "arkansas country", "auckland indie", "chamber psych", "redneck", "psychedelic rock", "math pop", "futuristic swag", "bachata dominicana", "classic garage rock", "beatlesque", "latin viral pop", "northern soul", "bedroom soul", "newfoundland indie", "indie cafe pop", "neo soul", "toronto indie", "electropowerpop", "drill", "memphis blues", "electronic rock", "punk blues", "birmingham metal", "norwegian singer-songwriter", "slowcore", "conscious hip hop", "children's folk", "australian indie rock", "skate punk", "chill pop", "compositional ambient", "cyberpunk", "rap latina", "melodic metal", "philly rap", "indie poptimism", "metropopolis", "electroclash", "chiptune", "western mass indie", "partyschlager", "scorecore", "jangle pop", "toronto rap", "atl trap", "liquid funk", "chicago soul", "metal", "cowboy western", "alternative dance", "west coast rap", "middle earth", "canadian hip hop", "afrobeat", "grave wave", "country", "art pop", "nwobhm", "chicano rap", "latin pop", "australian indigenous", "perth indie", "vocal jazz", "canadian punk", "emo", "appalachian folk", "grindcore", "alabama metal", "polish rock", "st louis rap", "dallas indie", "us power metal", "old school thrash", "new orleans funk", "trap latino", "hardcore hip hop", "happy hardcore", "swamp pop", "modern blues rock", "elephant 6", "edmonton indie", "cologne hip hop", "minimal tech house", "french indietronica", "romanian pop", "south african pop", "c86", "jump blues", "pittsburgh rock", "american grindcore", "indie electronica", "dc hardcore", "cedm", "jewish hip hop", "lds youth", "wu fam", "r&b", "colombian pop", "stoner metal", "bass trap", "australian indie folk", "antiviral pop", "japanese alternative rock", "canadian old school hip hop", "nu disco", "english indie rock", "neo-synthpop", "alternative country", "welsh rock", "heartland rock", "ohio indie", "lovers rock", "jazz blues", "no wave", "italian adult pop", "mellow gold", "louisiana blues", "alternative pop rock", "neo-singer-songwriter", "baton rouge rap", "progressive jazz fusion", "bubblegum pop", "victoria bc indie", "sesame street", "deep southern trap", "deep tropical house", "portland indie", "neo-classical", "kansas city hip hop", "swedish progressive metal", "pop rock", "vapor trap", "philly soul", "rock-and-roll", "latin rock", "sacramento indie", "power thrash", "swedish indie pop", "pixie", "teen pop", "oklahoma country", "philly indie", "swedish indie rock", "future garage", "classic soul", "otacore", "swamp rock", "rhode island rap", "rock quebecois", "socal pop punk", "avant-garde jazz", "canadian ccm", "canadian contemporary country", "lo-fi emo", "hi-nrg", "dutch house", "dance rock", "mexican rock", "bedroom pop", "british soul", "pop dance", "uk noise rock", "manitoba indie", "nl folk", "experimental indie rock", "hopebeat", "k-rap", "harlem hip hop", "neue deutsche welle", "texas country", "big band", "american metalcore", "deep talent show", "modern funk", "gothenburg indie", "rhode island indie", "lilith", "canadian contemporary r&b", "pop", "jazz rap", "deep acoustic pop", "polish indie", "boy band", "australian country", "rock steady", "vancouver indie", "funk metal", "canadian rock", "tennessee hip hop", "old-time", "chicago indie", "celtic rock", "san diego rap", "alaska indie", "canadian electronic", "dutch indie rock", "welsh indie", "edm", "south african rock", "pagan black metal", "torch song", "modern indie pop", "bounce", "north east england indie", "sophisti-pop", "destroy techno", "sacramento hip hop", "lounge", "houston rap", "norwegian pop", "video game music", "mathcore", "southern hip hop", "danish metal", "traditional country", "austin americana", "latin", "jazz funk", "old school dancehall", "hip house", "dunedin indie", "garage psych", "minneapolis indie", "technical thrash", "polish indie rock", "bassline", "jazz trombone", "christian hip hop", "pei indie", "comic", "house", "acoustic blues", "danish pop", "miami hip hop", "garage rock", "anti-folk", "baltimore indie", "chill r&b", "world worship", "hamburg electronic", "bubblegum dance", "yodeling", "reggaeton", "australian indie", "emo punk", "brazilian hip hop", "country rap", "electropop", "rockabilly", "modern power pop", "roots rock", "meme rap", "deep house", "balearic", "disco", "synth funk", "texas latin rap", "indie r&b", "midwest emo", "halifax indie", "social media pop", "glee club", "reggae rock", "tropical", "french soundtrack", "progressive sludge", "chicago rap", "dreamo", "p funk", "michigan indie", "el paso indie", "polish pop", "american post-rock", "bay area indie", "neo-psychedelic", "k-pop girl group", "british indie rock", "french indie pop", "folk punk", "adult standards", "outlaw country", "nyc pop", "garage punk", "oxford indie", "harmonica blues", "k-pop", "piano blues", "uk dnb", "dfw rap", "texas blues", "folktronica", "indie punk", "drum and bass", "action rock", "new england emo", "modern rock", "downtempo", "liverpool indie", "bass house", "garage pop", "deep new americana", "cartoon", "australian dance", "electronica chilena", "scottish singer-songwriter", "triangle indie", "indie pop rap", "kansas indie", "stoner rock", "vapor twitch", "rock en espanol", "uk post-punk", "instrumental soul", "popping", "nottingham indie", "quebec indie", "christian rock", "new french touch", "morelos indie", "canadian metal", "uk funky", "lawrence ks indie", "memphis indie", "g funk", "swedish synthpop", "cello", "dmv rap", "uk house", "brooklyn indie", "indiecoustica", "puerto rican pop", "bass music", "ann arbor indie", "rock drums", "grime", "glitch", "eurovision", "tech house", "baroque pop", "women's music", "spanish pop", "progressive house", "operatic pop", "big beat", "canadian country", "polish black metal", "modern alternative pop", "uk hip hop", "french synthpop", "indie garage rock", "funk rock", "symphonic power metal", "roots worship", "australian trap", "lgbtq+ hip hop", "uk alternative pop", "york indie", "rock keyboard", "traditional folk", "trap queen", "electric blues", "sleaze rock", "power metal", "bachata", "progressive metal", "soundtrack", "hamburger schule", "hardcore punk", "neo classical metal", "rap metal", "japanese post-hardcore", "bluegrass", "melodic metalcore", "polish alternative", "pop emo", "old school hip hop", "mexican classic rock", "complextro", "permanent wave", "goregrind", "acid rock", "technical death metal", "alternative hip hop", "modern dream pop", "viral rap", "girl group", "indie soul", "nashville hip hop", "death metal", "experimental pop", "country road", "swedish garage rock", "trap soul", "australian psych", "geek rock", "classic rock", "folk-pop", "neon pop punk", "progressive rock", "double drumming", "polish metal", "leeds indie", "zolo", "southampton indie", "future house", "norwegian space disco", "leicester indie", "dance-punk", "pop chileno", "pop punk", "black metal", "modern country rock", "new romantic", "kentucky roots", "christian alternative rock", "azonto", "melbourne bounce", "scandipop", "japanese vgm", "indie anthem-folk", "progressive death metal", "bubblegrunge", "athens indie", "omaha indie", "detroit hip hop", "technical grindcore", "hip hop", "album rock", "underground hip hop", "german reggae", "seattle hip hop", "rap", "minneapolis sound", "danish rock", "alberta country", "etherpop", "smooth jazz", "jazz fusion", "freak folk", "post-rock", "industrial metal", "candy pop", "rock", "irish rock", "hyphy", "slow game", "dream pop", "country pop", "san marcos tx indie", "queer country", "freakbeat", "north carolina hip hop", "trancecore", "indietronica", "preschool children's music", "australian talent show", "finnish edm", "classic canadian rock", "funk carioca", "acoustic pop", "swedish metal", "charlottesville indie", "german techno", "british blues", "cool jazz", "chicago bop", "fort worth indie", "hamilton on indie", "organic house", "german dance", "neo mellow", "alternative emo", "noise punk", "soul jazz", "vocal harmony group", "brill building pop", "norwegian hip hop", "deep underground hip hop", "polish death metal", "broken beat", "chopped and screwed", "canadian singer-songwriter", "mississippi hip hop", "uk doom metal", "bmore", "icelandic rock", "deep euro house", "new wave pop", "kids dance party", "canadian electropop", "progressive post-hardcore", "soul blues", "gospel r&b", "new weird america", "british singer-songwriter", "palm desert scene", "stomp and holler", "electronic trap", "british alternative rock", "modern reggae", "celtic punk", "easycore", "atlanta metal", "atlanta punk", "bow pop", "ectofolk", "garage rock revival", "bitpop", "irish singer-songwriter", "jam band", "psychedelic hip hop", "trance", "kindie rock", "ohio hip hop", "doo-wop", "pittsburgh rap", "glam rock", "nz pop", "polish alternative rock", "singer-songwriter", "atl hip hop", "british folk", "brutal death metal", "uk worship", "detroit rock", "nyc rap", "comedy rap", "eau claire indie", "milwaukee indie", "seattle indie", "minimal techno", "melodic death metal", "new jersey indie", "finnish metal", "boy pop", "frankfurt electronic", "electro house", "kentucky hip hop", "hollywood", "psychedelic folk", "viral pop", "belgian pop", "pop soul", "swedish death metal", "soca", "country rock", "modern alternative rock", "tropical house", "cambridgeshire indie", "alternative pop", "dutch trance", "scottish indie", "uplifting trance", "norwegian indie", "dutch hip hop", "grunge pop", "industrial rock", "dance pop", "christian music", "madchester", "afro dancehall", "progressive groove metal"]

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/allGenres')
def allGenres():
    # allGenreList = jsonify(allGenreList)
    return allGenreList

@app.route('/closest', methods=['GET'])
def closest():
    color = request.args['color']
    color = json.loads(color)
    closest = DB.get_closest_song(color['r'], color['g'], color['b']) # tools.getClosestSong(color['r'], color['g'], color['b'], color_df)
    closest['popularity'] = int(closest['popularity'])
    closest['R'] = int(closest['R'])
    closest['G'] = int(closest['G'])
    closest['B'] = int(closest['B'])

    print(closest)

    # closest = json.dumps(closest)    # print(request.args['color'])
    return jsonify({"results":closest})

@app.route('/genre', methods=['GET'])
def genre():
<<<<<<< HEAD
    genre = request.args['genre']
    print(genre)
    topN = tools.getGenreTopN(genre, color_df, 10)
=======
    # genre = request.args['genre']
    topN = DB.get_songs_for_genre('british soul', 10) # tools.getGenreTopN('british soul', color_df, 10)
>>>>>>> 67cf0fc6650ec261a2e3a983be8fa0d41d2fec37
    print(topN)
    return jsonify({"results":topN})

@app.route('/artist', methods=['GET'])
def artist():
    artist =  DB.get_songs_for_artist('Adele', 10) # tools.getArtistColor('Adele', color_df)
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