#!/usr/bin/env python

import subprocess
import optparse
import re


# Creates parser options, user input, return parser args.
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Pleae specify a new mac, use --help for more info.")
    return options


# Function to change MAC address.
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



# FINAL UPDATE

# Algorithm to check if MAC address was changed.
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(" [-] Could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# Calling function + w/options from user input.
change_mac(options.interface, options.new_mac)

# Check if current mac is what user requested.
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(" [+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")


