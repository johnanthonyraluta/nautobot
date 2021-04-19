import pynautobot
from modules.render_template import render_template
import json
from data_output import region_list
import pandas as pd
import sys


nautobot = pynautobot.api(
    url="http://10.66.69.142:8481/",
    token="5af16d6a2ffa79f62103139d2414d0f214edc7ad")

def devices():
    my_devices = nautobot.dcim.devices
    render_devices = render_template()
    to_add_devices = render_devices.devices()
    for devices in to_add_devices:
        try:
            print(devices)
            devices_conv = json.loads(devices)
            add_devices = my_devices.create(json.loads(devices))
        except:
            print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
    print("Done")

def region():
    my_region = nautobot.dcim.regions
    render_region = render_template()
    to_add_region = render_region.region()
    for regions in to_add_region:
        regions_conv = json.loads(regions)
        add_region = my_region.create(json.loads(regions))
    print("Done")

def roles():
    my_roles = nautobot.dcim.device_roles
    render_roles = render_template()
    to_add_roles = render_roles.roles()
    for roles in to_add_roles:
        print(roles)
        roles_conv = json.loads(roles)
        add_roles = my_roles.create(json.loads(roles))
    print("Done")

def interface():
    my_interface = nautobot.dcim.interfaces
    render_interfaces = render_template()
    to_add_interfaces = render_interfaces.interfaces()
    for interfaces in to_add_interfaces:
        try:
            print(interfaces)
            interfaces_conv = json.loads(interfaces)
            add_interfaces = my_interface.create(json.loads(interfaces))
        except:
            print('Cannot upload ' + interfaces)
    print("Done")

def ipam():
    my_ipadd = nautobot.ipam.ip_addresses
    render_ipadd = render_template()
    to_add_ipadd = render_ipadd.ipadd_be()

    for ipadd in to_add_ipadd:
        try:
            print(ipadd)
            ipadd_conv = json.loads(ipadd)
            add_ipadd = my_ipadd.create(json.loads(ipadd))
        except:
            print('Cannot upload ' + ipadd)
    print("Done")

def update_device():
    my_devices = nautobot.dcim.devices.get("69335dae-0cf6-4fdb-8780-a04b7f46fa40")
    render_devices = render_template()
    to_add_devices = render_devices.patch_devices()
    for devices in to_add_devices:
        try:
            print(devices)
            add_devices = my_devices.update(json.loads(devices))
        except:
            print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
    print("Done")

def inventory():
    my_inventory = nautobot.dcim.inventory_items
    render_devices = render_template()
    to_add_inventory = render_devices.inventory()
    for inventory in to_add_inventory:
        # try:
        add_inventory = my_inventory.create(json.loads(inventory))
        # except:
        #     print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
    print("Done")

def main():
    try:
        sys.argv[1]
    except:
        print(
            "Please input task (device,region,roles,interface,ipam,update_device,inventory) e.g. python ingest_data.py update_device")
        sys.exit(1)
    input = sys.argv[1]

    if input == "device":
        device()
    if input == "region":
        region()
    if input == "roles":
        roles()
    if input == "interface":
        interface()
    if input == "ipam":
        ipam()
    if input == "update_device"
        update_device()
    if input == "inventory":
        inventory()

if __name__ == '__main__':
    main()