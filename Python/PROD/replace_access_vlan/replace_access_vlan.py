if __name__ == "__main__":

    from netmiko import Netmiko, NetMikoAuthenticationException
    import getpass
    import time
    from inventory import devices

    print("\n\n##########################\nSSH to chosen host to change interface access vlans\n##########################\n\nUse at own discretion, if it creates a robot uprising thats on you man\n(only device in inventory is TESTSWT01 for testing) \n")


    while True:

        target_device = input("Name of Switch? (example: **):\n")
        if target_device.lower() in ["exit", "quit"]:
            print("Exiting..")
            exit(0)

        password = getpass.getpass("Device Password (user: admin):\n")

        if target_device in devices:
            device_info = devices[target_device]
            connection_info = device_info["connection"]
            connection_info["password"] = password
            try:
                print(f"\n***Connecting to {target_device} ({connection_info['host']})...")
                net_connect = Netmiko(**connection_info)
                net_connect.enable()
            except NetMikoAuthenticationException:
                print("\nAuthentication Failed")
                exit(1)

            # Pull the FULL running config
            output = net_connect.send_command("show running-config")
            
            # Parse interface blocks and find ones containing 'switchport access vlan 40'
            interfaces = []
            current_intf = None

            for line in output.splitlines():
                if line.startswith("interface "):
                    current_intf = line.split()[1]
                elif "switchport access vlan 40" in line and current_intf:
                    interfaces.append(current_intf)
                elif not line.startswith(" ") and not line.startswith("!"):
                    current_intf = None  # left the interface block

            print(f"\nInterfaces using VLAN 40")
            print("-" * 30)

            if interfaces:
                print(f"\nFound {len(interfaces)} interfaces:\n")
                for intf in interfaces:
                    print(f"  {intf}")
            else:
                print("No interfaces found using VLAN 40")

            continue_prompt = input("Press Enter to continue with operation if interfaces are correct (type 'exit' to quit): ")
            if continue_prompt.lower() == 'exit':
                print("Exiting..")
                exit(0)

            commands = []

            for intf in interfaces:
                commands += [
                    f"interface {intf}",
                    "switchport access vlan 45",
                ]
            
            if commands:
                result = net_connect.send_config_set(commands)
                print(result)

            


