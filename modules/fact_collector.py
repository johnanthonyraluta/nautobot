from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
from inventory.dansalan_inv import host_list

file_path = "/home/users/jraluta/tnt_script/nautobot/"
def show_platform():
    node_list = []
    for host_ in host_list:
        try:
            host = host_.split()[0]
            print('Connecting to ' + host + '...')
            tnt_session = ConnectHandler(
                device_type="cisco_xr",
                host=host,
                username="cisco",
                password="T&T!@bd!@n-C!sc0",
            )
            plat = tnt_session.send_command("show platform",use_textfsm=True)
            tnt_session.disconnect()
            print('Disconnected ' + host + '...')
            plat_parsed = parse_output(platform="cisco_xr", command="show version", data=plat)
            new_list = [host,plat_parsed]
            node_list.append(new_list)
        except:
            print('Node ' + host.split()[0] + ' is unreachable')
            return None
    return node_list

def write_file(node_facts):  #node_facts in list [nodes,facts]
    with open(file_path + 'data_output/showplat_facts.csv', 'a', newline='') as file_out:
        file_out.writerow(nodes_facts)

def main():
    collect_fact = show_platform()
    if collect_fact is not None:
        for node_facts in collect_fact:
            write_file(node_facts)
    else:
        print('No facts collected')

if __name__ == '__main__':
    main()
