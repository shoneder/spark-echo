from flask import Flask,request
import sys
import requests


requests.packages.urllib3.disable_warnings()

app = Flask(__name__)
authorization = "notset"
lastmessage = "notset"

@app.route("/")
def hello():
    return "Hello World-deployed"

@app.route("/test")
def test():
    return "test/Hello World"

# Webhook page will trigger webhooks() function
@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        # Get the json data
        json = request.get_json()
        #print("json=%s"%json)
        # parse the message id, person id, person email, and room id
        message_id = json["data"]["id"]
        person_id = json["data"]["personId"]
        person_email = json["data"]["personEmail"]
        room_id = json["data"]["roomId"]

        # convert the message id into readable text
        message = getmessage(message_id)

        #message = "testlocal"
        #print(message)

        # check if the message is the command to get hosts
        if message == "datacenter":
            # post the list of hosts into the Spark room
            postmessage(person_id, person_email, room_id,"yes...we rock")
            #print ("austria123")
        elif message == "ping":
            postmessage(person_id, person_email, room_id, "pong")
            #print ("message")
        return message
    except:
        return "huch...something went wrong"


# the getmessage function
def getmessage(message_id):
    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer %s"%authorization

    # add authorization to the header
    header = {"Authorization": "%s" % token}

    # create request url using message ID
    get_message_url = "https://api.ciscospark.com/v1/messages/" + message_id

    # send the GET request and do not verify SSL certificate for simplicity of this example
    api_response = requests.get(get_message_url, headers=header, verify=False)

    # parse the response in json
    response_json = api_response.json()

    # get the text value from the response
    text = response_json["text"]

    # return the text value
    return text

# the post function
def postmessage(person_id, person_email, room_id, text):
    # define a variable for the hostname of Spark
    hostname = ""

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer %s"%authorization

    # add authorization to the header
    header = {"Authorization": "%s" % token, "content-type": "application/json"}

    # specify request url
    post_message_url = "https://api.ciscospark.com/v1/messages"

    # create message in Spark room
    payload = {
        "personId" : person_id,
        "personEmail" : person_email,
        "roomId" : room_id,
        "text" : text
    }

    # create POST request do not verify SSL certificate for simplicity of this example
    api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)

    # get the response status code
    response_status = api_response.status_code

    # return the text value
    print(response_status)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        authorization = sys.argv[1]
    else:
        authorization = 'unknown'
    app.run(debug=True,host='0.0.0.0')



