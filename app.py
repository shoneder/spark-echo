from flask import Flask,request
from apicem import APICBasicTools
import sys
import requests


requests.packages.urllib3.disable_warnings()

app = Flask(__name__)
authorization = "notset"
admins = "notset"
apic_user="user"
apic_password="password"
apicem = None
auto_text = ["pong",
             "yes...we rock",
             "you are admin",
             "we are good to talk to apic-em",
             "seems there is a problem to connect apic-em",
             "shouldn't you check for a service ticket on apic-em?"
             ]

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

        person_email_id = person_email.split("@")[0]

        # convert the message id into readable text
        message = getmessage(message_id)

        #message = "testlocal"
        #print(message)

        # check if the message is the command to get hosts
        if message == "datacenter":
            # post the list of hosts into the Spark room
            postmessage(room_id,"yes...we rock")
            #print ("austria123")
        elif message == "ping":
            postmessage( room_id, "pong")
        elif person_email_id in admins:
            #note that we are admin
            if message in auto_text:
                return
            else:
                postmessage(room_id,"you are admin")

            # apicem routine
            if message == "apicem?":
                resp = apicem.getServiceTicket()
                if resp:
                    postmessage(room_id,"we are good to talk to apic-em")
                else:
                    postmessage(room_id,"seems there is a problem to connect apic-em")
            elif message.startswith("apicem:"):
                if apicem._ticket == None:
                    postmessage(room_id,"shouldn't you check for a service ticket on apic-em?")
                else:
                    cmd = message.split("apicem:")[1]
                    resp = apicem.doRestCall("get","/api/v1/network-device/%s"%cmd)
                    postmessage(room_id,"we received:%s"%resp)
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
def postmessage( room_id, text):
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
    if len(sys.argv) > 4:
        authorization = sys.argv[1]
        admins = sys.argv[2].split(",")
        apic_user = sys.argv[3]
        apic_password = sys.argv[4]
    else:
        authorization = 'unknown'
    apicem = APICBasicTools("sandboxapic.cisco.com:9443",apic_user,apic_password)
    app.run(debug=True,host='0.0.0.0')



