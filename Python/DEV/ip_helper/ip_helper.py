import requests, json, urllib3
urllib3.disable_warnings()               # suppress self-signed cert warnings

HOST = "***"                      # switch mgmt IP/FQDN
USER = "***"
PWD  = "***"
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# 1. pull **all** interface data from the native model
url = f"https://{HOST}/restconf/data/Cisco-IOS-XE-native:native/interface"
resp = requests.get(url, auth=(USER, PWD), headers=HEADERS, verify=False)
resp.raise_for_status()
interfaces = resp.json()["Cisco-IOS-XE-native:interface"]

matches = []

# 2. helper to walk any interface type
def check_if_type(if_dict, if_type):
    for entry in if_dict.get(if_type, []):
        ip = entry.get("ip", {})
        helper = ip.get("helper-address", {})
        # native model stores helpers as {"address":[{"address":"x.x.x.x"}]}
        if helper.get("address"):
            matches.append({
                "type": if_type,
                "name": entry["name"],
                "helpers": [h["address"] for h in helper["address"]]
            })

for t in interfaces.keys():
    check_if_type(interfaces, t)

print(json.dumps(matches, indent=2))