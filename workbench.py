import pynautobot
from modules.render_template import render_template
import json
from data_output import region_list
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# nautobot = pynautobot.api(
#     url="http://10.66.69.142:8481/",
#     token="5af16d6a2ffa79f62103139d2414d0f214edc7ad")
nautobot = pynautobot.api(
    url="http://10.66.69.149:8481/",
    token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
#
# to_add_device = {
#   "name": "TestDevice2",
#   "device_type": {"model":"aaa","slug":"ncs"},
#   "device_role": {"name":"bbb","slug":"an"},
#   "serial": "123abc",
#   "asset_tag": "string",
#   "site": {"name":"TestSite","slug":"testsite"},
#  "status": "Active"
# }
#
# devices = nautobot.dcim.devices
#
# device = nautobot.dcim.devices
# add_device = device.create(to_add_device)
# print(add_device.serial)

# my_region = nautobot.dcim.regions
# render_region = render_template()
# to_add_region = render_region.region()
# for regions in to_add_region:
#     regions_conv = json.loads(regions)
#     add_region = my_region.create(json.loads(regions))
# print("Done")

# my_roles = nautobot.dcim.device_roles
# render_roles = render_template()
# to_add_roles = render_roles.roles()
# for roles in to_add_roles:
#     print(roles)
#     roles_conv = json.loads(roles)
#     add_roles = my_roles.create(json.loads(roles))
# print("Done")

# my_devices = nautobot.dcim.devices
# render_devices = render_template()
# to_add_devices = render_devices.devices()
# for devices in to_add_devices:
#     try:
#         print(devices)
#         devices_conv = json.loads(devices)
#         add_devices = my_devices.create(json.loads(devices))
#     except:
#         print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
# print("Done")

# my_interface = nautobot.dcim.interfaces
# render_interfaces = render_template()
# to_add_interfaces = render_interfaces.interfaces()
# for interfaces in to_add_interfaces:
#     try:
#         print(interfaces)
#         interfaces_conv = json.loads(interfaces)
#         add_interfaces = my_interface.create(json.loads(interfaces))
#     except:
#         print('Cannot upload ' + interfaces)
# print("Done")

# my_ipadd = nautobot.ipam.ip_addresses
# render_ipadd = render_template()
# to_add_ipadd = render_ipadd.ipadd()
# for ipadd in to_add_ipadd:
#     try:
#         print(ipadd)
#         ipadd_conv = json.loads(ipadd)
#         add_ipadd = my_ipadd.create(json.loads(ipadd))
#     except:
#         print('Cannot upload ' + ipadd)
# print("Done")

# my_ipadd = nautobot.ipam.ip_addresses
# render_ipadd = render_template()
# to_add_ipadd = render_ipadd.ipadd_be()
#
# for ipadd in to_add_ipadd:
#     try:
#         print(ipadd)
#         ipadd_conv = json.loads(ipadd)
#         add_ipadd = my_ipadd.create(json.loads(ipadd))
#     except:
#         print('Cannot upload ' + ipadd)
# print("Done")

#updated devices
# my_devices = nautobot.dcim.devices.get("69335dae-0cf6-4fdb-8780-a04b7f46fa40")
# render_devices = render_template()
# to_add_devices = render_devices.patch_devices()
# for devices in to_add_devices:
#     try:
#         print(devices)
#         add_devices = my_devices.update(json.loads(devices))
#     except:
#         print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
# print("Done")

# my_inventory = nautobot.dcim.inventory_items
# render_devices = render_template()
# to_add_inventory = render_devices.inventory()
# for inventory in to_add_inventory:
#     # try:
#     add_inventory = my_inventory.create(json.loads(inventory))
#     # except:
#     #     print('Cannot upload '+devices + '. Check for duplicates or hostname in wrong format!')
# print("Done")

# from ntc_templates.parse import parse_output
# from netmiko import ConnectHandler
#
# tnt_session = ConnectHandler(
#     device_type="cisco_xr",
#     host="10.205.254.69",
#     username="cisco",
#     password="T&T!@bd!@n-C!sc0",
# )
# plat = tnt_session.send_command("show platform",use_textfsm=True)
# tnt_session.disconnect()
# plat_parsed = parse_output(platform="cisco_xr", command="show version", data=plat)


# plat = [{'location': '0/2/CPU0', 'card_type': 'NC55-36X100G-A-SE'}, {'location': '0/2/NPU0', 'card_type': 'Slice'}, {'location': '0/2/NPU1', 'card_type': 'Slice'}, {'location': '0/2/NPU2', 'card_type': 'Slice'}, {'location': '0/2/NPU3', 'card_type': 'Slice'}, {'location': '0/3/1', 'card_type': 'NC55-MPA-12T-S'}, {'location': '0/3/2', 'card_type': 'NC55-MPA-4H-S'}, {'location': '0/3/CPU0', 'card_type': 'NC55-MOD-A-SE-S'}, {'location': '0/3/NPU0', 'card_type': 'Slice'}, {'location': '0/RP0/CPU0', 'card_type': 'NC55-RP-E(Active)'}, {'location': '0/RP1/CPU0', 'card_type': 'NC55-RP-E(Standby)'}, {'location': '0/FC0', 'card_type': 'NC55-5504-FC'}, {'location': '0/FC1', 'card_type': 'NC55-5504-FC'}, {'location': '0/FC2', 'card_type': 'NC55-5504-FC'}, {'location': '0/FC3', 'card_type': 'NC55-5504-FC'}, {'location': '0/FC4', 'card_type': 'NC55-5504-FC'}, {'location': '0/FC5', 'card_type': 'NC55-5504-FC'}, {'location': '0/FT0', 'card_type': 'NC55-5504-FAN'}, {'location': '0/FT1', 'card_type': 'NC55-5504-FAN'}, {'location': '0/FT2', 'card_type': 'NC55-5504-FAN'}, {'location': '0/PM0', 'card_type': 'NC55-PWR-3KW-DC'}, {'location': '0/PM1', 'card_type': 'NC55-PWR-3KW-DC'}, {'location': '0/PM2', 'card_type': 'NC55-PWR-3KW-DC'}, {'location': '0/PM3', 'card_type': 'NC55-PWR-3KW-DC'}, {'location': '0/SC0', 'card_type': 'NC55-SC'}, {'location': '0/SC1', 'card_type': 'NC55-SC'}]
# for p in plat:
#     if '5504' in p['card_type']:
#         print('This is 5504 ' + p['card_type'] + ' at ' + p['location'])
#         break
#     if '5508' in p['card_type']:
#         print('This is 5508 ' + p['card_type']+ ' at ' + p['location'])
#         break
#     if '9910' in p['card_type']:
#         print('This is ASR-9910 ' + p['card_type']+ ' at ' + p['location'])
#         break
#
# ==============parse show platform====
#run this to collect show plat details
# import pandas as pd
# import ast
#
# show_list = []
# df = pd.read_csv("C:\\Users\\jraluta\\nautobot\data_output\\showplat_facts_pilot.csv")
# for plat in df['MODULES']:
#     res = ast.literal_eval(plat)
#     for p in res:
#         if '9910' in p['card_type']:
#             show_list.append("ASR9910")
#             print('ASR9910' )
#             break
#         if '5504' in p['card_type']:
#             show_list.append("NCS5504")
#             print('NCS5504')
#             break
#         if '5508' in p['card_type']:
#             show_list.append("NCS5508")
#             print('NCS5508')
#             break
#         if 'IOSXRV9000' in p['card_type']:
#             show_list.append("VM")
#             print('VM')
#             break
# df["PLATFORM"] = show_list
# pd.DataFrame(df).to_csv("C:\\Users\\jraluta\\nautobot\data_output\\showplat_facts.csv", index=False)
# ======merge two df based on hostname==
# df = pd.read_csv("data_input\\site_info.csv")
# df1 = pd.read_csv("data_output\\showplat_facts_pilot.csv")
#
# result = pd.merge(df, df1, how='left',on=["HOSTNAME","HOSTNAME"])
# result['PLATFORM'] = result['PLATFORM'].fillna('TBA')
# #final_result = result[['SITE_NAME','HOSTNAME','PLATFORM']]
# for index,row in result.iterrows():
#     print(row['HOSTNAME'],row['PLATFORM'],row['SITE_NAME'])

#
# ============
# how to get device id list:
# nautobot = pynautobot.api(
#     url="http://10.66.69.142:8481/",
#     token="5af16d6a2ffa79f62103139d2414d0f214edc7ad")
#
# device = nautobot.dcim.devices
# for dev in devices:
#     print(dev,dev.id)
# sample output
# AGSPXAGSCICU001 955a2e48-096d-432e-9679-fe8b25222ccd
# ALF00634CICN001 a2696a91-8828-430f-9d9a-2d148f3e793f
# ALF00634CICN002 4ca8dfcc-3f45-4146-87fe-633f64d9be52
# ALM00C07CICN001 5d33249d-f522-4f4c-9d9c-eb16a1f97d22

# =====
# #to get interface id and device list
# interface_id_prod = pd.DataFrame()
# my_interface = nautobot.dcim.interfaces
# for interface in my_interface.all():
#     print("Proccessing for interface " + interface.id)
#     if interface == "Loopback0" or interface =="Loopback1":
#         continue
#     int_dict = {"results__id":interface.id,"device/id":interface.device.id,"HOSTNAME":interface.device,"results__name":interface}
#     interface_id_prod = interface_id_prod.append(int_dict,ignore_index=True)
#     print("Done for interface " + interface.id)
# interface_id_prod.to_csv('data_input/interface_id_prod.csv', index=False)
# print('All Done!')
# sample output:
# Loopback0 b689997b-6ee0-4ff9-bd8f-0113812a5cf6 AGSPXAGSCICU001
# Loopback1 ee73fe77-3527-4a40-87a9-a4780dcddfc0 AGSPXAGSCICU001
# Loopback0 430d6459-d87c-4e17-9134-9b900ace1156 ALF00634CICN001

