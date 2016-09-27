from netmiko import ConnectHandler
import getpass
import os

USERNAME = input("Enter your username: ")
PASSWORD = getpass.getpass("Enter your password: ")

devices = open('devices.txt','r').read()
devices = devices.strip()
devices = devices.splitlines()

success = 0
failure = 0
unreachable = 0

for device in devices:
    try:
        net_connect = ConnectHandler(device_type='cisco_ios_ssh', ip=device, username=USERNAME, password=PASSWORD)
        net_connect.config_mode()
        if net_connect.check_config_mode() is True:
            net_connect.disconnect()
            print ("SUCCESS " + device)
            success += 1
        else:
            print ("FAILURE " + device)
            failure += 1
    except:
        print ("Unable to reach device " + device)
        unreachable += 1

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("Results")
print("Successful: " + str(success))
print("Failures: " + str(failure))
print("Unable to Reach: " + str(unreachable))
