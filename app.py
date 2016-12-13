#!/usr/bin/env python

import json
import os
import requests

from flask import Flask
from flask import make_response
from flask import request



# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST', 'PATCH'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "rallyGetStoryDetails" or \
        req.get("result").get("action") != "rallyUpdateState":
        return {}
    #baseurl = "http://localhost:8888/userstory/"
    baseurl = "https://rallyhelper3.herokuapp.com/userstory/"
    parameters = req.get("result").get("parameters")
    userStoryNumber = parameters.get("UsNumber")
    
    
    if req.get("result").get("action") != "rallyGetStoryDetails":
        resp = requests.get(baseurl+"US"+userStoryNumber,
                headers={'Content-Type': 'Application/Json'})
        response = json.loads(resp.text)
        print response
    
    if req.get("result").get("action") != "rallyUpdateState":
        state = parameters.get("State")
        print state
        payload = {"state": state}
        resp = requests.patch(baseurl+userStoryNumber, 
                    headers={'Content-Type': 'Application/Json'},
                    data=json.dumps(payload))
        response = json.loads(resp.text)
        print response
    
    finalResp =  makeWebhookResult(response)   
    return finalResp

def makeWebhookResult(resp):
    
    storyName = resp['storyName']
    if storyName is None:
        return {}
    
    storyScheduledState = resp['storyScheduledState']
    if storyScheduledState is None:
        return {}
    
    storyOwner = resp['storyOwner']
    if storyOwner is None:
        return {}
    
    storyDescription = resp['storyDescription']
    if storyDescription is None:
        return {}
    
    storyAssignedTeam = resp['storyAssignedTeam']
    if storyAssignedTeam is None:
        return {}
    
    storyRef = resp['storyRef']
    if storyRef is None:
        return {}
    

    speech = "UserStory: " + storyName + ": " + "State:" + storyScheduledState +\
             ", Story Owner: " + storyOwner + " Assigned To: " + storyAssignedTeam

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "spark-apiai-rally"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='localhost')
