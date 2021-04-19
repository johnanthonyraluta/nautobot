from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
from inventory.nodes_inventory import host_list
import csv

file_path = "/home/users/jraluta/tnt_script/nautobot/"
def show_platform():
    node_list = []
    for host_ in host_list:
        try:
            host = host_.split()[1]
            print('Connecting to ' + host + '...')
            tnt_session = ConnectHandler(
                device_type="cisco_xr",
                host=host,
                username="pldtadmin",
                password="3nter_Me-1n2admin",
            )
            plat = tnt_session.send_command("show platform",use_textfsm=True)
            tnt_session.disconnect()
            print('Disconnected ' + host + '...')
            new_list = [host_.split()[0],plat]
            node_list.append(new_list)
        except:
            print('Node ' + host.split()[0] + ' is unreachable')
    return node_list

def write_file(node_facts):  #node_facts in list [nodes,facts]
    with open(file_path + 'data_output/showplat_facts_pilot.csv', 'a', newline='') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(node_facts)

def main():
    collect_fact = show_platform()
    if collect_fact is not None:
        for node_facts in collect_fact:
            print(node_facts)
            write_file(node_facts)
    else:
        print('No facts collected')
    print('Facts collection done!')
if __name__ == '__main__':
    main()
