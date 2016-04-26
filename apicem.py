# Login + Service Ticket Receive
# Basic RestCall with return of json


import requests
import json
import sys

requests.packages.urllib3.disable_warnings()  # Disable warnings

#CONTROLLER_IP = "sandboxapic.cisco.com:9443"
GET = "get"
POST = "post"
DELETE = "delete"


class APICBasicTools(object):
    _ticket = None
    _controllerIP = None
    _username = None
    _password = None
    _logger = None

    def __init__(self,controllerIP, username, password):
        self._controllerIP = controllerIP
        self._username=username
        self._password=password


    def getServiceTicket(self):
        ticket = None
        # specify the username and password which will be included in the data.  Replace ‘xxxx’ with
        #your username and password
        payload = {"username": self._username, "password": self._password}

        #This is the URL to get the service ticket.
        #The base IP call is https://[Controller IP]/api/v1
        #The REST function is ‘ticket’
        url = "https://" + self._controllerIP + "/api/v1/ticket"

        #Content type must be included in the header
        header = {"content-type": "application/json"}

        #Format the payload to JSON and add to the data.  Include the header in the call.
        #SSL certification is turned off, but should be active in production environments
        response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

        #Check if a response was received. If not, print an error message.
        if (not response):
            return False
        else:
            #Data received.  Get the ticket and print to screen.
            r_json = response.json()
            ticket = r_json["response"]["serviceTicket"]
        self._ticket = ticket
        return True


# Make the REST call using the service ticket, command, http url, data for the body (if any)
    def doRestCall(self, command, apiurl, aData=None):
        response_json = None
        payload = None
        try:

            #if data for the body is passed in put into JSON format for the payload
            if (aData != None):
                payload = json.dumps(aData)

            #add the service ticket and content type to the header
            header = {"X-Auth-Token": self._ticket, "content-type": "application/json"}
            url = "https://" + self._controllerIP + "%s" % apiurl
            if (command == GET):
                r = requests.get(url, data=payload, headers=header, verify=False)
            elif (command == POST):
                r = requests.post(url, data=payload, headers=header, verify=False)
            #elif (command == DELETE):
            #    r = requests.delete(url, data=payload, headers = header, verify = False)
            else:
                #if the command is not GET or POST we don’t handle it.
                return

            response_json = r.json()
            return response_json;
        except:
            err = sys.exc_info()[0]
            msg_det = sys.exc_info()[1]

