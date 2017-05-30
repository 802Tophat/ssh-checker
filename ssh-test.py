from __future__ import absolute_import, division, print_function

from netmiko import ConnectHandler
from getpass import getpass
import os
import signal
import sys

#signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
#signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    """Prompt for and return a username and password."""
    USERNAME = get_input('Enter Username: ')
    PASSWORD = None
    while not PASSWORD:
        PASSWORD = getpass()
        password_verify = getpass('Retype your password: ')
        if PASSWORD != password_verify:
            print('Passwords do not match.  Try again.')
            PASSWORD = None
    return USERNAME, PASSWORD

USERNAME, PASSWORD = get_credentials()

devices = open('devices.txt','r').read()
devices = devices.strip()
devices = devices.splitlines()

success = 0
failure = 0
unreachable = 0

for device in devices:
    try:
        net_connect = ConnectHandler(device_type='cisco_ios_ssh', ip=device,
                                     username=USERNAME, password=PASSWORD)
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
