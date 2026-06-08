if __name__ == "__main__":

    from netmiko import Netmiko, NetMikoAuthenticationException
    import getpass
    import time
    from inventory import devices

    print("\n\n##########################\nTHIS SCRIPT WILL SSH TO CHOSEN DEVICE, REMOVE CURRENT IP-HELPERS AND ADD NEW ONES (proper SVIs and new ip-helper addresses are pre-scripted)\n##########################\n\nUse at own discretion, if it creates a robot uprising thats on you man\n(only device in inventory is TESTSWT01 for testing) \n")


    while True:

        target_device = input("Name of Switch? (example: **):\n")
        if target_device.lower() in ["exit", "quit"]:
            print("Exiting..")
            exit(0)

        password = getpass.getpass("Device Password (user: **):\n")

        new_helpers = [
                "192.168.2.3",
                "192.168.2.4"
            ]

        if target_device in devices:
            device_info = devices[target_device]
            interface = device_info["interface"]
            connection_info = device_info["connection"]
            connection_info["password"] = password
            try:
                print(f"\n***Connecting to {target_device} ({connection_info['host']})...")
                net_connect = Netmiko(**connection_info)
                net_connect.enable()
            except NetMikoAuthenticationException:
                print("\nAuthentication Failed")
                exit(1)

            print(f"\n***Checking current config on interface {interface}..\n")
            time.sleep(2)
            output = net_connect.send_command(f"show run interface {interface}")
            print(output)
            print(f"***New ip-helpers will be {new_helpers}\n")
            continue_prompt = input("Press Enter to continue with removal/addition of helpers (type 'exit' to quit): ")
            if continue_prompt.lower() == 'exit':
                print("Exiting..")
                exit(0)

            config_lines = output.splitlines()
            config_commands = [f"interface {interface}"]

            for line in config_lines:
                if "ip helper-address" in line:
                    existing_ip = line.strip().split()[-1]
                    config_commands.append(f"no ip helper-address {existing_ip}")
                    print(f"\nFound existing helper-address(s): {existing_ip}")
                    time.sleep(1)
                    print(f"***Removing..")

            for helper in new_helpers:
                config_commands.append(f"ip helper-address {helper}")

            net_connect.send_config_set(config_commands)
            print(f"\n***Adding new ip-helpers: {new_helpers}")
            time.sleep(2)

            print(f"\n***Config complete, showing result..\n")
            time.sleep(1)
            final = net_connect.send_command(f"show run interface {interface}")
            print(final)
            final_prompt = input("Press Enter to save config to startup (type 'exit' to quit): ")
            if final_prompt == "exit":
                exit()
            else:
                net_connect.send_command("wr")
                print("\nSaving...\n")
            net_connect.disconnect()


