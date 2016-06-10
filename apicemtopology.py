import os
import random
from apicem import APICBasicTools
import requests
import json
import sys
import pprint


requests.packages.urllib3.disable_warnings()  # Disable warnings

#CONTROLLER_IP = "sandboxapic.cisco.com:9443"
GET = "get"
POST = "post"
DELETE = "delete"


class APICEMTopologyWrapper(object):
    _basicTools = None
    _physicalTopology = "/api/v1/topology/physical-topology"
    _mapFamilyToIcon = {
        "routers":"router",
        "switches and hubs":"switch",
        "unified ap":"accesspoint",
        "wireless controller":"wlc",
        "wired":"host",
        "cloud node":"cloud",
        "firewall":"firewall",
        "wireless":"wirelesshost"

    }


    def __init__(self,controllerIP, username, password):
        self._basicTools = APICBasicTools(controllerIP,username,password)
        if self._basicTools.getServiceTicket() == False:
            return "Error occured"

    def getNextTopology(self):
        resp=self.getPhysicalTopology()
        return self.convertTopologyToNext(resp)

    def getPhysicalTopology(self):
        topology = None
        result = self._basicTools.doRestCall(GET,self._physicalTopology)
        #f = open("sample.response",'r')
        #result = json.load(f)
        #f.close()
        print(result)
        topology=result["response"]
        return topology

    def convertTopologyToNext(self, apic_topology):
        next_topology = apic_topology
        apic_node_id_mapping = {}
        apic_link_id_mapping = {}
        node_id = 0
        link_id = 0
        family = ""
        for i in range(0,len(apic_topology["nodes"])) :
            apic_node_id_mapping[apic_topology["nodes"][i]["id"]] = node_id
            next_topology["nodes"][i]["id"] = node_id
            #next_topology["nodes"][i]["x"] = random.randint(1, 800)
            #next_topology["nodes"][i]["y"] = random.randint(1, 400)
            node_id+=1
            if "family" in apic_topology["nodes"][i].keys():
                if apic_topology["nodes"][i]["family"].lower() in self._mapFamilyToIcon.keys():
                    next_topology["nodes"][i]["icon"] = self._mapFamilyToIcon[apic_topology["nodes"][i]["family"].lower()]


        for i in range(0,len(apic_topology["links"])) :
            if ("id" in next_topology["links"][i].keys()):
                apic_link_id_mapping[apic_topology["links"][i]["id"]] = link_id

            next_topology["links"][i]["id"] = link_id
            next_topology["links"][i]["source"] = apic_node_id_mapping[apic_topology["links"][i]["source"]]
            next_topology["links"][i]["target"] = apic_node_id_mapping[apic_topology["links"][i]["target"]]
            link_id+=1

        #pprint.pprint(next_topology)
        return next_topology



  #  switch
  #  router
  #  wlc
  #  unknown
  #  server
  #  phone
  #  nexus5000
  #  ipphone
  #  host
  #  camera
  #  accesspoint

