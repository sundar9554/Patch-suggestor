import requests
import sys
import pdb
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
#from lxml import html
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

patches = {'16.3.2': ['CSCvp12345', 'CSCvn34213', 'CSCv074761'], 'Everest-16.6.5':['CSCvo34343', 'CSCum12123', 'CSCun87467']}
def ret_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    return device_list

def get_sw_version():
    """
    Getting software version of all the available devices
    """
    done = False
    if len(sys.argv) != 2:
        print("Give hostname of the device please!")
        return
    in_host = sys.argv[1]
    #device_list = ret_device_list()
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    for device in device_list['response']:
        if str(device['hostname']) != in_host:
            continue
        device_ip = device['managementIpAddress']
        url = "https://sandboxdnac.cisco.com/api/v1/network-device/ip-address/" + device_ip
        hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
        resp = requests.get(url, headers=hdr)  # Make the Get Request
        image_details = resp.json()
        sw_version = image_details['response']['softwareVersion']
        print("Host: " + in_host + " IP: " + device_ip + " software version: " + sw_version + "\n")

        # Now suggest the patches

        print("You need the following Patches: ") 
        print(patches[sw_version])
        #pdb.set_trace()
        #page = requests.get('https://wwwin-ottawa.cisco.com/tfoggoa/Scrubber/showquery.html?query=tmondal-7')
        #processed_page = BeautifulSoup(page.content, 'html.parser') 
    #page = requests.get('http://www.fabpedigree.com/james/mathmen.htm')
    #processed_page = BeautifulSoup(page.content, 'html.parser')
        #for td in processed_page.select('td'):
        #    print(td.text)

#print 'Patches: ', ddts

def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use


if __name__ == "__main__":
    get_sw_version()

