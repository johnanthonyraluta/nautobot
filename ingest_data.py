import pynautobot
from modules.render_template import render_template
import json
from data_output import region_list
import pandas as pd
import sys


nautobot = pynautobot.api(
    url="http://10.66.69.149:8481/",
    token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

def devices():
    my_devices = nautobot.dcim.devices
    render_devices = render_template()
    to_add_devices = render_devices.devices()
    for devices in to_add_devices:
        try:
            print(devices)
            devices_conv = json.loads(devices)
            add_devices = my_devices.create(devices_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def region():
    my_region = nautobot.dcim.regions
    render_region = render_template()
    to_add_region = render_region.region()
    for regions in to_add_region:
        add_region = my_region.create(regions)
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

def sites():
    my_sites = nautobot.dcim.sites
    render_sites = render_template()
    to_add_sites = render_sites.sites()
    for sites in to_add_sites:
        try:
            print(sites)
            sites_conv = json.loads(sites)
            add_sites = my_sites.create(sites_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def loopback():
    my_interface = nautobot.dcim.interfaces
    render_interfaces = render_template()
    to_add_interfaces = render_interfaces.loop_interfaces()
    for interfaces in to_add_interfaces:
        try:
            print(interfaces)
            interfaces_conv = json.loads(interfaces)
            add_interfaces = my_interface.create(interfaces_conv)
        except:
            print('Cannot upload ' + interfaces)
    print("Done")

def ipadd_loop():
    my_ipadd = nautobot.ipam.ip_addresses
    render_ipadd = render_template()
    to_add_ipadd = render_ipadd.ipadd_loopback()

    for ipadd in to_add_ipadd:
        try:
            print(ipadd)
            ipadd_conv = json.loads(ipadd)
            add_ipadd = my_ipadd.create(ipadd_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def assign_primary():
    my_primary = nautobot.dcim.devices.get("33e89bbe-6da2-411e-9fca-7792a66b22bf")
    render_primary = render_template()
    to_add_primary = render_primary.patch_devices()
    for pri in to_add_primary:
        try:
            print(pri)
            pri_conv = json.loads(pri)
            add_primary = my_primary.update(pri_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def ipadd_be():
    my_ipadd = nautobot.ipam.ip_addresses
    render_ipadd = render_template()
    to_add_ipadd = render_ipadd.ipadd_be()
    for ipadd in to_add_ipadd:
        try:
            print(ipadd)
            ipadd_conv = json.loads(ipadd)
            add_ipadd = my_ipadd.create(ipadd_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def update_device():
    my_devices = nautobot.dcim.devices.get("33e89bbe-6da2-411e-9fca-7792a66b22bf")
    render_devices = render_template()
    to_add_devices = render_devices.patch_devices()
    for devices in to_add_devices:
        try:
            print(devices)
            add_devices = my_devices.update(json.loads(devices))
        except:
            print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
    print("Done")

def update_custom():
    my_custom = nautobot.dcim.devices.get("33e89bbe-6da2-411e-9fca-7792a66b22bf")
    render_custom = render_template()
    to_add_custom = render_custom.custom_field()
    for fields in to_add_custom:
        try:
            print(fields)
            add_custom = my_custom.update(json.loads(fields))
        except:
            print('Cannot upload '+fields + '.')
    print("Done")

def inventory():
    my_inventory = nautobot.dcim.inventory_items
    render_devices = render_template()
    to_add_inventory = render_devices.inventory()
    for inventory in to_add_inventory:
        try:
            print(inventory)
            add_inventory = my_inventory.create(json.loads(inventory))
        except pynautobot.RequestError as e:
            print(e.error)
            pass
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
        devices()
    if input == "region":
        region()
    if input == "roles":
        try:
            roles()
        except:
            print('Aborted!')
    if input == "loopback":
        loopback()
    if input == "ipadd_loop":
        ipadd_loop()
    if input == "assign_primary":
        assign_primary()
    if input == "ipadd_be":
        ipadd_be()
    if input == "custom":
        update_custom()
    if input == "inventory":
        inventory()
    if input == "sites":
        sites()

if __name__ == '__main__':
    main()