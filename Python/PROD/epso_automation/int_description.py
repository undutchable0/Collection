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
    descrip_num = 71


    net_connect = Netmiko(**switch["connection"])
    net_connect.enable()

#flr position interfaces switch01 1 -10
    while int_num <= 7:
        config = [f"interface g1/0/{int_num}", f"description POS{descrip_num:02}", "switchport access vlan 62"]
        
        send_config = net_connect.send_config_set(config)
        print(send_config)

        int_num += 2
        descrip_num += 2

# flr position interfaces switch02 1-10

    int_num = 2
    descrip_num = 71

    while int_num <= 8:
        config = [f"interface g1/0/{int_num}", f"description POS{descrip_num:02} Phone", "switchport access vlan 162"]
        
        send_config = net_connect.send_config_set(config)
        print(send_config)

        int_num += 2
        descrip_num += 2

    int_num = 1
    descrip_num = 72

    while int_num <= 9:
        config = [f"interface g2/0/{int_num}", f"description POS{descrip_num:02}", "switchport access vlan 62"]
        
        send_config = net_connect.send_config_set(config)
        print(send_config)

        int_num += 2
        descrip_num += 2

#sup position interfaces switch02 11-14

    int_num = 2
    descrip_num = 72

    while int_num <= 10:
        config = [f"interface g2/0/{int_num}", f"description POS{descrip_num:02} Phone", "switchport access vlan 162"]
        
        send_config = net_connect.send_config_set(config)
        print(send_config)

        int_num += 2
        descrip_num += 2

# #flr position phones switch01 2-20

#     int_num = 2
#     descrip_num = 2

#     while int_num <= 25:
#         config = [f"interface g1/0/{int_num}", f"description POS{descrip_num:02} Phone"]
        
#         send_config = net_connect.send_config_set(config)
#         print(send_config)

#         int_num += 2
#         descrip_num += 2

# #flr position phones switch02 15-25

#     int_num = 15
#     descrip_num = 2

#     while int_num <= 25:
#         config = [f"interface g2/0/{int_num}", f"description PHONE{descrip_num:02}"]
        
#         send_config = net_connect.send_config_set(config)
#         print(send_config)

#         int_num += 1
#         descrip_num += 2

# #sup position phones switch01 

#     int_num = 26
#     descrip_num = 51

#     while int_num <= 36:
#         config = [f"interface g1/0/{int_num}", f"description PHONE{descrip_num:02}"]
        
#         send_config = net_connect.send_config_set(config)
#         print(send_config)

#         int_num += 1
#         descrip_num += 2

# #sup position phones switch02

#     int_num = 26
#     descrip_num = 52

#     while int_num <= 36:
#         config = [f"interface g2/0/{int_num}", f"description PHONE{descrip_num:02}"]
        
#         send_config = net_connect.send_config_set(config)
#         print(send_config)

#         int_num += 1
#         descrip_num += 2


    net_connect.disconnect()
    exit(0)
    print("\n~~Finished")



