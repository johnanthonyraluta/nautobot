import pynautobot
from modules.render_template import render_template
import json
from data_output import region_list
import pandas as pd
import sys

error_log = open("errors_ingest_data.log", "w")

nautobot = pynautobot.api(
    url="http://10.66.69.149:8481/",
    token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

# nautobot = pynautobot.api(
#     url="http://10.66.69.142:8481/",
#     token="5af16d6a2ffa79f62103139d2414d0f214edc7ad")

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

def physical_interface():
    my_phy = nautobot.dcim.interfaces
    render_phy = render_template()
    to_add_phy = render_phy.phy_int()
    for phy in to_add_phy:
        try:
            print(phy)
            phy_conv = json.loads(phy)
            add_phy = my_phy.create(phy_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def connect_cables():
    my_conn = nautobot.dcim.cables
    render_conn = render_template()
    to_add_conn = render_conn.add_connection()
    for conn in to_add_conn:
        conn_conv = json.loads(conn)
        source = nautobot.dcim.interfaces.get(name=conn_conv["termination_a_id"][0], device=conn_conv["termination_a_id"][1])
        target = nautobot.dcim.interfaces.get(name=conn_conv["termination_b_id"][0], device=conn_conv["termination_b_id"][1])
        if source != None:
            conn_conv["termination_a_id"] = source.id
        if target != None:
            conn_conv["termination_b_id"] = target.id
        try:
            print(conn_conv)
            add_conn = my_conn.create(conn_conv)
            print ("Done with " + str(source) + " " + str(target))
        except pynautobot.RequestError as e:
            error_log.write("{0} {1}\n{2}\n".format(source, target, str(e.error)))
            print(source, target)
            print(e.error)
            pass

def interface_shut():
    my_phy = nautobot.dcim.interfaces
    render_phy = render_template()
    to_add_phy = render_phy.shut_interfaces()
    for phy in to_add_phy:
        try:
            print(phy)
            phy_conv = json.loads(phy)
            #my_phy = nautobot.dcim.interfaces.get(device=phy_conv["device"]["name"],name=phy_conv["name"])
            add_phy = my_phy.create(phy_conv)
            #add_phy = my_phy.update(phy_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def rt():
    my_rt = nautobot.ipam.route_targets
    render_rt = render_template()
    to_add_rt = render_rt.rt()
    for rt in to_add_rt:
        rt_conv = json.loads(rt)
        try:
            dup_rt = nautobot.ipam.route_targets.get(name=rt_conv["name"])
        except:
            continue
        if dup_rt == None:
            try:
                print(rt)
                add_rt = my_rt.create(rt_conv)
            except pynautobot.RequestError as e:
                print(e.error)
                pass
        else:
            print("Duplicated RT " + str(dup_rt))
    print("Done")

def assign_rt():
    render_rt = render_template()
    to_add_rt = render_rt.assign_rt()
    for rt in to_add_rt:
        print(rt)
        rt_conv = json.loads(rt)
        try:
            dup_rt = nautobot.ipam.vrfs.get(import_targets=rt_conv["import_targets"],export_targets=rt_conv\
                ["export_targets"])
        except:
            dup_rt = None
            pass
        if dup_rt == None:
            my_rt = nautobot.ipam.vrfs.get(name=rt_conv["name"])
            if my_rt != None:
                rt_ex_list = []
                rt_imp_list = []
                for rt_ex in rt_conv["export_targets"]:
                    print(rt_ex)
                    rt_export = nautobot.ipam.route_targets.get(name=rt_ex)
                    rt_ex_id = rt_export.id
                    rt_ex_list.append(rt_ex_id)
                for rt_imp in rt_conv["import_targets"]:
                    print(rt_imp)
                    rt_import = nautobot.ipam.route_targets.get(name=rt_imp)
                    rt_imp_id = rt_import.id
                    rt_imp_list.append(rt_imp_id)
                rt_conv["export_targets"] = rt_ex_list
                rt_conv["import_targets"] = rt_imp_list
                print(rt_conv)
                # try:
                add_rt = my_rt.update(rt_conv)
                print("Done for " + rt_conv["name"])
            # except pynautobot.RequestError as e:
            #     print(e.error)
            #     pass
            else:
                continue
        else:
            print("Duplicated RT " + str(dup_rt))
    print("Done")

def vrf():
    my_vrf = nautobot.ipam.vrfs
    render_vrf = render_template()
    to_add_vrf = render_vrf.vrf()
    for vrf in to_add_vrf:
        vrf_conv = json.loads(vrf)
        dup_vrf = nautobot.ipam.vrfs.get(name=vrf_conv["name"])
        if dup_vrf == None:
            try:
                print(vrf)
                add_vrf = my_vrf.create(vrf_conv)
            except pynautobot.RequestError as e:
                print(e.error)
                pass
        else:
            print("Duplicated vrf " + str(dup_vrf))
    print("Done")

def vrf_assignment():
    render_vrf = render_template()
    to_add_vrf = render_vrf.assign_vrf()
    for vrf in to_add_vrf:
        vrf_conv = json.loads(vrf)
        try:
            vrf_dup = nautobot.ipam.ip_addresses.get(device=vrf_conv["dns_name"], interface=vrf_conv["description"])
        except:
            pass
        print(vrf_dup)
        if vrf_dup == None:
            print("Cannot assign vrf to " + vrf_conv["dns_name"] + " with interface " + \
                  vrf_conv["description"])
        elif vrf_dup.vrf == None and vrf_dup != None:
            if vrf_conv["address"] in str(vrf_dup):
                address_ = str(vrf_dup)
                try:
                    my_vrf = nautobot.ipam.ip_addresses.get(address=address_)
                    vrf_conv["address"] = address_
                    vrf_conv["dns_name"] = " "
                    vrf_conv["description"] = " "
                    print(vrf_conv)
                    add_vrf = my_vrf.update(vrf_conv)
                except pynautobot.RequestError as e:
                    print(e.error)
                    pass
        else:
            print("Duplicated vrf " + vrf_conv["dns_name"])
    print("Done")

def vlan():
    my_vlan = nautobot.ipam.vlans
    render_vlan = render_template()
    to_add_vlan = render_vlan.vlan()
    for vlan in to_add_vlan:
        vlan_conv = json.loads(vlan)
        dup_vlan = nautobot.ipam.vlans.get(name=vlan_conv["name"])
        if dup_vlan == None:
            try:
                print(vlan)
                add_vlan = my_vlan.create(vlan_conv)
            except pynautobot.RequestError as e:
                print(e.error)
                pass
        else:
            print("Duplicated vlan " + str(dup_vlan))
    print("Done")

def assign_vlan():
    render_vlan = render_template()
    to_add_vlan = render_vlan.assign_vlan()
    for vlan in to_add_vlan:
        print(vlan)
        vlan_conv = json.loads(vlan)
        try:
            vlan_dup = nautobot.dcim.interfaces.get(device=vlan_conv["device"]["name"], interface=vlan_conv["name"],\
                                                    vlan=vlan_conv["untagged_vlan"])
        except:
            pass
        print(vlan_dup)
        # if vlan_dup == None:
        #     print("Cannot assign vlan to " + vlan_conv["device"]["name"] + " with interface " + \
        #           vrf_conv["name"])
        if vlan_dup == None:
            my_vlan = nautobot.ipam.vlans.get(name=vlan_conv["untagged_vlan"])
            my_vlan_int = nautobot.dcim.interfaces.get(name=vlan_conv["name"],\
                                                      device=vlan_conv["device"]["name"])
            vlan_conv["untagged_vlan"] = my_vlan.id
            print(vlan_conv)
            if my_vlan_int != None:
                try:
                    add_vlan = my_vlan_int.update(vlan_conv)
                except pynautobot.RequestError as e:
                    error_log.write("{0} {1}\n{2}\n".format(vlan_conv["name"], vlan_conv["device"]["name"], str(e.error)))
                    print(e.error)
                    pass
            else:
                error_log.write("Hostname " + vlan_conv["device"]["name"] + " and/or interface " + \
                      vlan_conv["name"] + " is not yet defined.\n")
                print("Hostname " + vlan_conv["device"]["name"] + " and/or interface " + \
                      vlan_conv["name"] + " is not yet defined.")
        else:
            error_log.write("Duplicated vlan of " + vlan_conv["device"]["name"] + " " + vlan_conv["name"] + " " + \
                            vlan_conv["untagged_vlan"] + "\n")
            print("Duplicated vlan of " + vlan_conv["device"]["name"] + " " + vlan_conv["name"] + " " + vlan_conv["untagged_vlan"])
    print("Done")

def bundle_interface():
    my_be = nautobot.dcim.interfaces
    render_be = render_template()
    to_add_be = render_be.be_int()
    for be in to_add_be:
        try:
            print(be)
            be_conv = json.loads(be)
            add_be = my_be.create(be_conv)
        except pynautobot.RequestError as e:
            print(e.error)
            pass
    print("Done")

def ipadd_be():
    my_ipadd = nautobot.ipam.ip_addresses
    render_ipadd = render_template()
    to_add_ipadd = render_ipadd.ipadd_be()
    for ipadd in to_add_ipadd:
        ipadd_conv = json.loads(ipadd)
        #print(ipadd_conv)
        bundle = nautobot.dcim.interfaces.get(name=ipadd_conv["assigned_object"]["name"], device=ipadd_conv["assigned_object"]["device"]["name"])
        print(bundle)
        try:
            dup_ip = my_ipadd.get(assigned_object_id=bundle.id, address=ipadd_conv["address"])
        except:
            print("No address or no interface defined!")
        if bundle != None and dup_ip == None:
            print(bundle.id)
            ipadd_conv['assigned_object']['id'] = bundle.id
            ipadd_conv['assigned_object_id'] = bundle.id
            print(ipadd_conv)
        # try:
            add_ipadd = my_ipadd.create(ipadd_conv)
        # except pynautobot.RequestError as e:
        #     print(e.error)
        #     pass
        elif bundle == None:
            print("No defined interface bundle")
        elif dup_ip != None:
            print("Duplicate IP " + ipadd_conv['address'])
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
            inventory_conv = json.loads(inventory)
            device = nautobot.dcim.devices.get(name=inventory_conv["device"]["name"])
            inventory_conv["device"]["id"] = device.id
            print(inventory_conv)
            add_inventory = my_inventory.create(inventory_conv)
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
    if input == "physical_interface":
        physical_interface()
    if input == "connect":
        connect_cables()
    if input == "interface_shut":
        interface_shut()
    if input == "bundle_interface":
        bundle_interface()
    if input == "ipadd_be":
        ipadd_be()
    if input == "custom":
        update_custom()
    if input == "inventory":
        inventory()
    if input == "sites":
        sites()
    if input == "vrf":
        vrf()
    if input == "assign_vrf":
        vrf_assignment()
    if input =="rt":
        rt()
    if input =="assign_rt":
        assign_rt()
    if input == "vlan":
        vlan()
    if input == "assign_vlan":
        assign_vlan()
    if input == "inventory":
        inventory()

if __name__ == '__main__':
    main()