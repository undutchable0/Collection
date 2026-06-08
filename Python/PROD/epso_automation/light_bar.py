if __name__ == "__main__":

    from netmiko import Netmiko, NetMikoAuthenticationException
    import getpass

    print("*" * 20, "\nThis script will modify description on chosen interfaces\n~by Renz aka straight killa\n" + "*" * 20)

    password = getpass.getpass("\nDevice Password:")

    switch = {
        "connection": {
            "host": "**",
            "username": "**",
            "password": **,
            "device_type": "cisco_ios",
            "global_delay_factor": 0.1,

        }

    }

    int_num = 1
    descrip_num = 1


    net_connect = Netmiko(**switch["connection"])
    net_connect.enable()

    while int_num <= 20:
        config = [f"interface g1/0/{int_num}", f"description LIGHT{descrip_num:02}", "switchport access vlan 62"]
        
        send_config = net_connect.send_config_set(config)
        print(send_config)

        int_num += 1
        descrip_num += 1


    net_connect.disconnect()
    exit(0)
    print("\n~~Finished")
