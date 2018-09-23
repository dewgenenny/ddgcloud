from __future__ import print_function
import socket
import time
import json
import logging
from google.cloud import dns
import google.cloud
import urllib
import urllib.request

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

try:
    fileopen = open("host_list", "r")
    
    hosts_to_update = fileopen.read().splitlines()
except:
    print ("Oops no host_list")

import logging
logging.basicConfig(filename='dns_updater.log',level=logging.DEBUG)


FIVE_MINUTES = 5 * 60

#client = dns.Client.from_service_account_json('/home/tom/coding/docker_gcloud_dns/client_secrets.json')



domain = 'tom-george.com'

def hostname_resolves(hostname):
    try:
        print("Looking up: "+hostname)
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

def updateDNS(record, ip):
    client = dns.Client.from_service_account_json('/home/tom/coding/docker_gcloud_dns/client_secrets.json')
    zone = client.zone('tomgeorge')

    full_record = record + '.tom-george.com.'
    
    if hostname_resolves(full_record) == 1:
        record_set = zone.resource_record_set(full_record, 'A', FIVE_MINUTES, [ip,])
        old_record_set = zone.resource_record_set(full_record, 'A', FIVE_MINUTES, [socket.gethostbyname(full_record),]) 
        changes = zone.changes()
        changes.delete_record_set(old_record_set)  # API request
        changes.add_record_set(record_set)
    else:
        record_set = zone.resource_record_set(full_record, 'A', FIVE_MINUTES, [ip,])
        changes = zone.changes()
        changes.add_record_set(record_set)

    changes.create()  # API request
    while changes.status != 'done':
        logging.info('Waiting for changes to complete')
        time.sleep(5)     # or whatever interval is appropriate
        changes.reload()   # API request
        logging.info('Changes completed')




with urllib.request.urlopen("http://wtfismyip.com/json") as url:
    ip = url.read()
encoding = url.info().get_content_charset('utf-8')
JSON_object = json.loads(ip.decode(encoding))
print (JSON_object['YourFuckingIPAddress'])


try:
    mfip = JSON_object['YourFuckingIPAddress']
    #print (mfip)
except Exception as e:
    print (e)

for host in hosts_to_update:
   print("Updating: "+host+" IP:"+mfip)
   updateDNS(host, mfip)


