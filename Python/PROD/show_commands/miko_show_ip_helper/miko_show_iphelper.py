from netmiko import Netmiko
from inventory import devices

for name, host in devices.items():
    net_connect = Netmiko(**host)
    output = net_connect.send_command("show ip helper-address", use_textfsm=True)

    with open("show_iphelper.txt", "a") as f:
        print(f"[+]Switch: {name} ({host['host']})")
        print("---------------")
        print(output, "\n")

        print(f"[+]Switch: {name} ({host['host']})", file=f)
        print("---------------", file=f)
        print(output, "\n", file=f)

    net_connect.disconnect()
    

