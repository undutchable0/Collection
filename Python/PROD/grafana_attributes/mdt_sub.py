from ncclient import manager
import logging
import xmltodict
import json
from lxml.etree import fromstring

# logging.basicConfig(level=logging.DEBUG)

router = {
    "host": "**",
    "port": "830",
    "username": "**",
    "password": "**",
    "hostkey_verify": False,
    "device_params": {"name": "csr"}
}


with manager.connect(**router) as m:
    subs = ["/interfaces-ios-xe-oper:interfaces/interface/statistics"]
    for sub in subs:
        rpc = f"""
            <establish-subscription xmlns='urn:ietf:params:xml:ns:yang:ietf-event-notifications' xmlns:yp='urn:ietf:params:xml:ns:yang:ietf-yang-push'>
                <stream>yp:yang-push</stream>
                <yp:xpath-filter>{sub}</yp:xpath-filter>
                <yp:period>500</yp:period>
            </establish-subscription>
        """
        response = m.dispatch(fromstring(rpc))
        python_resp = xmltodict.parse(response.xml)
        # print(python_resp['rpc-reply']['subscription-result']['#text'])
        # print(python_resp['rpc-reply']['subscription-id']['#text'])

        while True:
            sub_data = m.take_notification()
            python_sub_data = xmltodict.parse(sub_data.notification_xml)
            print(json.dumps(python_sub_data, indent=2))
            json_str = json.dumps(python_sub_data, indent=2)
            with open("output.txt", "a") as f:
                f.write(json_str)
                f.write("\n")
            # print(
            #     f"Sub ID: {python_sub_data['notification']['push-update']['subscription-id']}")
            # # print(python_sub_data)
            # print(
            #     f"Name: {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['name']}")
            # print(
            #     f"Total RAM: {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['total-memory']}")
            # print(
            #     f"Used RAM: {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['used-memory']}")
            # print(
            #     f"Free RAM: {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['free-memory']}")
