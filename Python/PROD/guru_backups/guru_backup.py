import json
import requests
import json
import base64

print("\n\n##########################\nGURU BACKUP\n##########################\n")
print("script by Rens, aka straightkilla ~\n")

base_url = "https://api.getguru.com/api/v1"

collections = "/collections"

username = input("Guru accnt email username: ")
key = input("Guru User API key: ")


api_key = f"{username}:{key}"

encoded_key = base64.b64encode(api_key.encode()).decode()

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {encoded_key}"
}

response = requests.get(base_url+collections, headers=headers).json()



for collection in response:
    # print(json.dumps(collection["id"], indent=2))
    id = collection["id"]
    export = requests.post(url=f"{base_url}/collections/{id}/export/advanced", headers=headers)
    print(f"{collection["name"]}: {id} **EXPORTED")
    print(export)

print("\n~~Backups for all collections should be received through email within a few minutes")

