from requests import session
import os
import sys
import ipaddress
import json


def isYes(i):
    return i == "" or i.lower() in ["y", "yes"]


def isNo(i):
    return i == "" or i.lower() in ["n", "no"]


def getIp(s):
    while True:
        ip = input(s)
        try:
            return ipaddress.ip_address(ip)
        except ValueError:
            print("Wrong input")

class Network:

    def __init__(self, data=None):
        if None:
            pass

class Node:

    def __init__(self, data=None):
        pass



class ZeroTier(object):

    def __init__(self, host="http://127.0.0.1:9993"):
        self.host = "http://127.0.0.1:9993"
        self.r = session()

    def _loadToken(self):
        if os.geteuid() != 0:
            os.execvp("sudo", ["sudo"] + sys.argv)
        token = open("/var/lib/zerotier-one/authtoken.secret").read()
        self.r.headers['X-ZT1-Auth'] = token

    def getStatus(self):
        data = r.get(self.host + "/status").json()
        if data['version']:
            print("Version:", data['version'])
            self.address = data['address']
            self.r = r
            ret = self.r.get(self.host + "/controller").json()
            self.controller = not ret['controller']
        else:
            print("Fail when talk with zerotier")
            sys.exit(1)


class ZeroTierController(ZeroTier):

    def getHostedNetworks(self):
        return self.r.get(self.host+"/controller/network").json()

    def getHostedNetworkInfo(self, nwid):
        return self.r.get(self.host+"/controller/network/"+nwid).json()

    def



class Application:

    def __init__(self):
        self.cfg = {}
        

    def loadToken(self):
        if os.geteuid() != 0:
            os.execvp("sudo", ["sudo"] + sys.argv)
        token = open("/var/lib/zerotier-one/authtoken.secret").read()

        self.r.headers['X-ZT1-Auth'] = token

        data = r.get(self.host + "/status").json()
        if data['version']:
            print("Version:", data['version'])
            self.address = data['address']
            self.r = r
            ret = self.r.get(self.host + "/controller").json()
            if not ret['controller']:
                print("The Node is not a controlle\nrecompile the package with 'ZT_ENABLE_NETWORK_CONTROLLER=1' can get you a controller")
                sys.exit(1)
        else:
            print("Fail when talk with zerotier")
            sys.exit(1)

    def getNwid(self):
        self.r.get(self.host + "/")

    def setNwid(self):
        nwid = input("Input the networkid [000000]:")
        self.nwid = self.address + nwid if nwid else self.address + "000000"
        print("The nwid is '{}'".format(self.nwid))

    def setName(self):
        self.cfg['name'] = input("Input the name for the network:")
        print("The name is set as '{}'".format(self.cfg['name']))

    def setPrivate(self):
        self.cfg['private'] = Bool(input("Is this network private?"))
        print("The network would be", "private" if self.cfg['private'] else "public")

    def setBroadCast(self):
        self.cfg['enableBroadcast'] = Bool(input("Allow the Ethernet broadcast?"))
        print("broadcast is", "enabled" if self.cfg['enableBroadcast'] else "disabled")

    def setallowPassiveBridging(self):
        self.cfg['allowPassiveBridging'] = Bool(input("Allow any member to bridge?"))
        print("PassiveBridging is", "enabled" if self.cfg['allowPassiveBridging'] else "disabled")

    def setv4AssignMode(self):
        if "ipAssignmentPools" not in self.cfg:
            self.cfg['ipAssignmentPools'] = []

        if "ipLocalRoutes" not in self.cfg:
            self.cfg['ipLocalRoutes'] = []

        self.cfg['v4AssignMode'] = input('Choose the v4AssignMode:[zt, none, dhcp]')
        if self.cfg['v4AssignMode'] == "dhcp":
            return
        if self.cfg['v4AssignMode'] == "zt":
            start = ip_input("Please input the start of the address:")
            end = ip_input("please input the end of the address:")
            self.cfg["ipAssignmentPools"].extend([str(ip) for ip in ipaddress.collapse_addresses([start, end])])
            self.cfg['ipLocalRoutes'].append({
                "ipRangeStart": str(start),
                "ipRangeEnd": str(end)
            })

        self.cfg['v4AssignMode'] == "none"

    def setv6AssignMode(self):
        self.cfg['v6AssignMode'] = input('Choose the v6AssignMode:[zt, none, dhcp]')
        if self.cfg['v6AssignMode'] == "dhcp":
            return
        if self.cfg['v6AssignMode'] == "zt":
            raise NotImplementedError
        self.cfg['v6AssignMode'] == "none"

    def setDefaultRule(self):
        self.cfg["rules"] = [{
            "ruleNo": 0,
            "nodeId": None,
            "sourcePort": None,
            "destPort": None,
            "vlanId": None,
            "vlanPcp": None,
            "etherType": None,
            "macSource": None,
            "macDest": None,
            "ipSource": None,
            "ipDest": None,
            "ipTos": None,
            "ipProtocol": None,
            "ipSourcePort": None,
            "ipDestPort": None,
            "action": "accept"
        }]
        # add a accept all rule

    def auth(self):
        i = input("ID of member")
        if i:
            self.r.post("http://127.0.0.1:9993/controller/network/{}/member/{}".format(self.cfg['nwid'], i), data=json.dumps({
                "authorized": True
            }))
    # def setmulticastLimit(self):
    #     self.cfg['multicastLimit'] = input('input the multicastLimit[32]:')

    def setrelays(self):
        input("Set the relays, input q to finish, input address,address to set a relay")
        to_set = True
        relays = []
        while to_set:
            i = input("TO")
            if i == "q":
                break
            else:
                relay = [j.strip() for j in i.split(".")]
                relays.append({
                    "address": relay[0],
                    "phyAddress": relay[1]
                })
        self.cfg["relays"] = relays

    def submit(self):
        ret = self.r.post("http://127.0.0.1:9993/controller/network/"+self.nwid, data=json.dumps(self.cfg)).json()
        print(ret)

if __name__ == '__main__':
    app = Application()
    app.loadToken()
    if len(sys.argv) == 1:
        print("usage:")
        print(__file__ + " new")
        print(__file__ + " relay")
        sys.exit(0)
    if sys.argv[1] == "new":
        print("Going to setup a new network, you are going through serveral questions.")
        app.setNwid()
        app.setName()
        app.setPrivate()
        app.setBroadCast()
        app.setallowPassiveBridging()
        app.setv4AssignMode()
        app.setv6AssignMode()
        app.setDefaultRule()
        app.submit()
    elif sys.argv[1] == "relay":
        print("Going to setup a new network, you are going through serveral questions.")
        app.setNwid()
        app.setrelays()
        app.submit()
    elif sys.argv[1] == "auth":
        app.setNwid()
        app.auth()
