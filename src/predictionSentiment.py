import imghdr
import requests
import json
from constants import EINSTEIN_LANGUAGE_URL

_PREDICTION_URL = EINSTEIN_LANGUAGE_URL +"/v2/language/sentiment"


def predict(token, text):
    """Run a prediction against a model using image url.

    Args:
        token: oauth token
        model_id: model id
        image_url: image url

    Returns:
        A json string containing classes and probabilities.
    """
    
    payload = {"modelId" : "CommunitySentiment","document" : text}

    #payload = {"modelId":"CommunitySentiment","document":"The presentation was great and I learned a lot"}
    headers = {
            'Authorization':'Bearer ' + token, 
            'Cache-Control': 'no-cache', 
            "Content-Type": "application/json"
            }
    
    return _prediction_request(_PREDICTION_URL, payload, headers)   

def _prediction_request(url, payload, headers):
    """Make a prediction request.
    Args:
        url: endpoint url
        data: multipart payload
        headers: request headers

    Returns:
        JSON response
    """    
    try:   
        response = requests.post(url, data = json.dumps(payload), headers=headers)
        return response
    except requests.exceptions.RequestException as exp:
        raise exp("Prediction failed: \"{}\"".format(response))
