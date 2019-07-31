from app import app
from flask import render_template, request
from app.models import model, formopener
import requests
from yelp.client import Client
from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'touristtrap' 

app.config['MONGO_URI'] = 'mongodb+srv://schan:ewb92XqWtPZEJDBb@cluster0-jrcsk.mongodb.net/touristtrap?retryWrites=true&w=majority'

mongo = PyMongo(app)

MY_API_KEY = "lunbRJRhsHamyVoTQ3qUNVvRBvcsbUv5sZxgaQg2BBaet4R7Wnqt1lfg4ES1eLMvH70r93X6B3KZ8cFAIRaYlZS_QWAOcXQ-3QoVQ2IOQckvk855i0WjIqKZruk-XXYx"
#  Replace this with your real API key

client = Client(MY_API_KEY)

# business_response = client.business.get_by_id('yelp-Times-Square')


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


def requestYelp(host, path, term, location, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = str(host) + str(path) + "?term=\"" + str(term) + "\"&location=\"" + str(location) + "\""
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...', url)

    response = requests.request('GET', url, headers=headers, params=url_params)
    
    

    return response.json()


def requestYelpReview(host, idef, api_key, url_params=None):

    url_params = url_params or {}
    url = str(host) + '/v3/businesses/' + idef + '/reviews'
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...', url)

    response = requests.request('GET', url, headers=headers, params=url_params)
    
    

    return response.json()


    # definitons 
    # TS = Times Square
    # SL = Statue of Liberty
    # ES = Ellis Island
    # LI = Little Italy
    # RC = Rockefeller Center
    # CP = Central Park
    # MB = Magnolia Bakery
    # CI = Coney Island
    
    
businessTS = requestYelp(API_HOST, SEARCH_PATH, "Times Square", "New York", MY_API_KEY)
businessSL = requestYelp(API_HOST, SEARCH_PATH, "Statue of Liberty", "New York", MY_API_KEY)
businessES = requestYelp(API_HOST, SEARCH_PATH, "Empire State Building", "New York", MY_API_KEY)
businessLI = requestYelp(API_HOST, SEARCH_PATH, "Little Italy", "New York", MY_API_KEY)
businessRC = requestYelp(API_HOST, SEARCH_PATH, "Rockefeller Center", "New York", MY_API_KEY)
businessCP = requestYelp(API_HOST, SEARCH_PATH, "Central Park", "New York", MY_API_KEY)
businessMB = requestYelp(API_HOST, SEARCH_PATH, "Magnolia Bakery", "New York", MY_API_KEY)
businessCI = requestYelp(API_HOST, SEARCH_PATH, "Coney Island", "New York", MY_API_KEY)
businessWTC = requestYelp(API_HOST, SEARCH_PATH, "One World Trade Center", "New York", MY_API_KEY)


businessIDTS = businessTS["businesses"][0]["id"]
businessIDSL = businessSL["businesses"][0]["id"]
businessIDES = businessES["businesses"][0]["id"]
businessIDLI = businessLI["businesses"][0]["id"]
businessIDRC = businessRC["businesses"][0]["id"]
businessIDCP = businessCP["businesses"][0]["id"]
businessIDMB = businessMB["businesses"][0]["id"]
businessIDCI = businessCI["businesses"][0]["id"]
businessIDWTC = businessWTC["businesses"][0]["id"]

REVIEW_PATH = '/v3/businesses/' + businessIDTS + '/reviews'

businessTSR = requestYelpReview(API_HOST, businessIDTS, MY_API_KEY)
reviewTS = businessTSR["reviews"]
businessSLR = requestYelpReview(API_HOST, businessIDSL, MY_API_KEY)
reviewSL = businessSLR["reviews"]
businessESR = requestYelpReview(API_HOST, businessIDES, MY_API_KEY)
reviewES = businessESR["reviews"]
businessLIR = requestYelpReview(API_HOST, businessIDLI, MY_API_KEY)
reviewLI = businessLIR["reviews"]
businessRCR = requestYelpReview(API_HOST, businessIDRC, MY_API_KEY)
reviewRC = businessRCR["reviews"]
businessCPR = requestYelpReview(API_HOST, businessIDCP, MY_API_KEY)
reviewCP = businessCPR["reviews"]
businessMBR = requestYelpReview(API_HOST, businessIDMB, MY_API_KEY)
reviewMB = businessMBR["reviews"]
businessCIR = requestYelpReview(API_HOST, businessIDCI, MY_API_KEY)
reviewCI = businessCIR["reviews"]
businessWTCR = requestYelpReview(API_HOST, businessIDWTC, MY_API_KEY)
reviewWTC = businessWTCR["reviews"]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# @app.route('/review/<place>')
# def reviewPage(place):
#     #api stuff
#     return render_template('reviews.html')
    
@app.route('/places')
def places():
    return render_template('places.html', businessTS = businessTS, businessCI = businessCI, 
    businessMB = businessMB, businessCP = businessCP, businessRC = businessRC, businessES = businessES, 
    businessSL = businessSL, businessLI = businessLI, businessWTC = businessWTC)

@app.route('/TSReviews')
def TSReviews():
    return render_template('TimesSquare.html', businessTSR = businessTSR, reviewTS = reviewTS)
    
@app.route('/SLReviews')
def SLReviews():
    return render_template('Liberty.html', businessSLR = businessSLR, reviewSL = reviewSL)

@app.route('/LIReviews')
def LIReviews():
    return render_template('LittleItaly.html', businessLIR = businessLIR, reviewLI = reviewLI)
    
@app.route('/ESReviews')
def ESReviews():
    return render_template('EmpireState.html', businessESR = businessESR, reviewES = reviewES)
    
@app.route('/RCReviews')
def RCReviews():
    return render_template('Rockefeller.html', businessRCR = businessRCR, reviewRC = reviewRC)
    
@app.route('/CPReviews')
def CPReviews():
    return render_template('CentralPark.html', businessCPR = businessCPR, reviewCP = reviewCP)
    
@app.route('/MBReviews')
def MBReviews():
    return render_template('Magnolia.html', businessMBR = businessMBR, reviewMB = reviewMB)

@app.route('/CIReviews')
def CIReviews():
    return render_template('ConeyIsland.html', businessCIR = businessCIR, reviewCI = reviewCI)
    
@app.route('/WTCReviews')
def WTCReviews():
    return render_template('wtc.html', businessWTCR = businessWTCR, reviewWTC = reviewWTC)


@app.route('/submittrap')
def submittrap():
    # connect to the database
    place = mongo.db.touristtrap
    
    # insert new data
    
    # return a message to the user
    return render_template('submittrap.html')
    
@app.route('/test')
def test():
    return render_template('test.html')
    
@app.route('/locationAdded', methods = ["GET", "POST"])
def locationAdded():
    if request.method == "POST":
        userData = dict(request.form)
        placeName = userData["placeName"]
        placeLocation = userData["placeLocation"]
        collection = mongo.db.touristtrap
        collection.insert({'placeName':placeName, 'placeLocation':placeLocation})
        return render_template("locationAdded.html")
    else:
        return "Please fill out the form."