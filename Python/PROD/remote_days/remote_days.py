import requests
import json
import base64
import sys
from datetime import datetime, timedelta

print("\n\n##########################\nTHIS SCRIPT WILL REQUEST REMOTE TIME OFF FROM BAMBOO, FOR THE CHOSEN DAY OF THE WEEK, FOR THE AMOUNT OF DAYS IN ADVANCE CHOSEN\n##########################\n")
print("script by Rens, aka straightkilla ~\n")

continue_prompt = input("Press Enter to continue (type 'exit' to quit): ")

if continue_prompt == "exit":
    sys.exit()

api_key_input = input("API Key?(obtain from Bamboo): ")

api_key = f"{api_key_input}:x"

encoded_key = base64.b64encode(api_key.encode()).decode()

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {encoded_key}"
}

employee_url = "https://api.bamboohr.com/api/gateway.php/elpasoteller911/v1/employees/directory"

response = requests.get(employee_url, headers=headers).json()

print("\n**EPTC911 BAMBOO EMPLOYEE ID NUMBERS**:\n")

for employee in response["employees"]:
    print(f"{employee['displayName']}: {employee['id']}")

employee_id = input("\nEmployee ID?: ")

base_url = f"https://api.bamboohr.com/api/gateway.php/elpasoteller911/v1/employees/{employee_id}/time_off/request" 

#obtain employee id with GET = https://api.bamboohr.com/api/gateway.php/elpasoteller911/v1/employees/directory


start_date_input = input("Start date of requests?(YYYY-MM-DD): ")
time_delta_input = int(input("How many days worth of requests beginning at start date?(ex: 60): "))


day_input = int(input("For what day of the week?(0=Mon, 6=Sun): "))


start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
end_date = start_date + timedelta(days=time_delta_input) 

current_date = start_date

while current_date <= end_date:
    if current_date.weekday() == day_input:
       date_str = current_date.strftime('%Y-%m-%d')

       payload = {
          "start": date_str,
          "end": date_str,
          "timeOffTypeId": 86,
          "amount": 8,
          "status": "requested"
       }

       response = requests.put(base_url, json=payload, headers=headers)

       print(f"Request for {date_str}= {response.status_code}")
       try:
           print("201 = Success")
       except json.JSONDecodeError:
           print("Response not valid JSON")
    current_date += timedelta(days=1)

last_prompt = input("Press Enter to end")
if continue_prompt == "exit":
    sys.exit()
