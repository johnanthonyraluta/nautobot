import csv
import json
import requests
import ast
from jinja2 import Environment, FileSystemLoader
from data_output.region_list import region_list
import pandas as pd
from netaddr import IPAddress
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

file_path = "C:\\Users\\jraluta\\nautobot\\"
device_list = []
roles_list = []
interface_list = []
ipadd_list = []
site_list = []
tmp_list = []
class render_template():

    def template(self,template_type,dict_type):
        file_loader = FileSystemLoader(file_path + "templates")
        env = Environment(loader=file_loader)
        template = env.get_template(template_type)
        output = template.render(dict_type)
        return output

    def region(self):
        region_dict = {}
        with open(file_path + "data_input\\regions.csv", encoding='utf-8-sig') as file:
            read = csv.reader(file)
            for r in read:
                v1 = r[0]
                v2 = r[1]
                v3 = r[2]
                region_dict = {'v1':v1,'v2':v2,'v3':v3}
                file_loader = FileSystemLoader(file_path + "templates")
                env = Environment(loader=file_loader)
                template = env.get_template("region.j2")
                output = template.render(region_dict)
                output = json.loads(output)
                region_list.append(output)
        return region_list

    def roles(self,template_type = "device-role.j2"):
        roles_dict = {}
        with open(file_path + "data_input\\roles.csv", encoding='utf-8-sig') as file:
            read = csv.reader(file)
            for r in read:
                v1 = r[0].strip()
                v2 = r[1].strip()
                v3 = r[2].strip()
                v4 = r[3].strip()
                v5 = r[4].strip()
                roles_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5}
                roles_output = self.template(template_type,roles_dict)
                roles_list.append(roles_output)
        return roles_list

    def sites(self,template_type = "sites.j2"):
        site_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df_new = df[['SITE_NAME','REGION']].drop_duplicates()
        df_new = df_new.dropna()
        for sites in df_new['SITE_NAME']:
            v1 = sites.strip()
            xform = sites.split()
            v2 = '-'.join(xform).lower()
            v3 = df_new.loc[df_new['SITE_NAME']==sites,'REGION'].iloc[0]
            v4 = v3.lower()
            site_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4}
            site_output = self.template(template_type,site_dict)
            site_list.append(site_output)
        return site_list

    def devices(self,template_type = "devices.j2"):
        device_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_output\\showplat_facts.csv")
        result = pd.merge(df, df1, how='left', on=["HOSTNAME", "HOSTNAME"])
        result['PLATFORM'] = result['PLATFORM'].fillna('TBA')
        for index, row in result.iterrows():
            v1=row['HOSTNAME'].strip()
            v2=row['PLATFORM'].strip()
            if 'RR' in row['DEVICE_TYPE']:
                v3= '_'.join(row['DEVICE_TYPE'].split('-')[:-1])
            else:
                v3=row['DEVICE_TYPE'].split('-')[0]
            v4=row['SITE_NAME'].strip()
            v5=row['IPV4_MANAGEMENT_IP'].strip()
            v6=row['IPV6_MANAGEMENT_IP'].strip()
            v7=row['IPV4_LOOPBACK0_ADDRESS'].strip()
            v8=row['PLATFORM'].lower().strip()
            v9=v3.lower().strip()
            v10_=v4.lower().strip()
            v10="-".join(v10_.split()).strip()
            device_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'v6':v6,'v7':v7,'v8':v8,\
                           'v9':v9,'v10':v10}
            device_output = self.template(template_type,device_dict)
            device_list.append(device_output)
        return device_list

    def patch_devices(self,template_type = "patch_devices.j2"):
        device_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_input\\interface_id_prod.csv")
        result = pd.merge(df, df1, how='left', on=["HOSTNAME", "HOSTNAME"])
        for index, row in result.iterrows():
            v1=row['HOSTNAME'].strip()
            v5=row['IPV4_MANAGEMENT_IP'].strip()
            v6=row['IPV6_MANAGEMENT_IP'].strip()
            v11=row["device/id"]
            device_dict = {'v1':v1,'v5':v5,'v6':v6,'v11':v11}
            device_output = self.template(template_type,device_dict)
            device_list.append(device_output)
        return device_list

    def custom_field(self,template_type = "custom.j2"):
        device_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_input\\interface_id_prod_loopback.csv")
        result = pd.merge(df, df1, how='left', on=["HOSTNAME", "HOSTNAME"])
        print(result.head())
        result["SID_ABSOLUTE_PREFIX"] = result["SID_ABSOLUTE_PREFIX"].fillna(0)
        result["SID_ABSOLUTE_STRICT_PREFIX"] = result["SID_ABSOLUTE_STRICT_PREFIX"].fillna(0)
        result["ANY_CAST_SID"] = result["ANY_CAST_SID"].fillna(0)
        result = result.astype({"SID_ABSOLUTE_PREFIX": int, "SID_ABSOLUTE_STRICT_PREFIX": int,\
                                 "ANY_CAST_SID":int},errors='ignore')
        print(result[["HOSTNAME", "SID_ABSOLUTE_PREFIX", "SID_ABSOLUTE_STRICT_PREFIX", "ANY_CAST_SID"]])
        for index, row in result.iterrows():
            v1=row['HOSTNAME'].strip()
            v8=row['SID_ABSOLUTE_PREFIX']
            v9=row['SID_ABSOLUTE_STRICT_PREFIX']
            v10=row['ANY_CAST_SID']
            v11=row["device/id"]
            v12=row["PHASE"]
            device_dict = {'v1':v1,'v8':v8,'v9':v9,'v10':v10,'v11':v11,'v12':v12}
            device_output = self.template(template_type,device_dict)
            device_list.append(device_output)
        return device_list

    def inventory(self,template_type = "inventory.j2"):
        tmp_dict = {}
        # df = pd.read_csv("data_output\\showplat_facts.csv")
        # df = df.dropna()
        # df1 = pd.read_csv("data_input\\interface_id_prod.csv")
        # df1 = df1.dropna()
        # #merge but just display the common outputs
        # #results = pd.merge(df, df1, how='left', on=["SOURCE_BUNDLE_INTERFACE", "SOURCE_BUNDLE_INTERFACE"])
        # results = df.merge(df1[['HOSTNAME','device/id']])
        # results = results.dropna()
        # results = results.drop_duplicates()
        # #print(results)
        # #print(resd)
        # for index, row in results.iterrows():
        #     v1=row['device/id']
        #     v2=row['HOSTNAME']
        #     modules=row['MODULES']
        #     #v2 = v2_.replace("'",'"')
        #     modules = ast.literal_eval(modules)
        #     for module in modules:
        #         v4 = module['location'].strip()
        #         v3 = module['card_type'].strip()
        #         device_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4}
        #         device_output = self.template(template_type,device_dict)
        #         device_list.append(device_output)
        df = pd.read_csv("data_input\\service_discovery_show_version.csv")
        results = df
        for index, row in results.iterrows():
            v1 = ""
            v2 = row["hostname"]
            v3 = row["name"]
            v4 = row["vid"]
            v5 = row["descr"]
            v6 = row["pid"]
            v7 = row["sn"]
            tmp_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'v6':v6,'v7':v7}
            tmp_output = self.template(template_type,tmp_dict)
            tmp_list.append(tmp_output)
            print("Done inventory " + v2)
        return tmp_list


    def loop_interfaces(self,template_type = "interface.j2"):
        interface_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        for index,row in df.iterrows():
            for i in range(2):
                v1 = row['HOSTNAME'].strip()
                #my_uuid = str(uuid.uuid4())
                if i == 0:
                    v2 = i
                    v3 = "default loopback"
                    #v4 = my_uuid
                    interface_dict = {'v1':v1,'v2':v2,'v3':v3}
                    interface_output = self.template(template_type,interface_dict)
                    interface_list.append(interface_output)
                    print(v1,v2,v3)
                if i == 1:
                    v2 = i
                    v3 = "network management loopback"
                    #v4 = my_uuid
                    interface_dict = {'v1':v1,'v2':v2,'v3':v3}
                    interface_output = self.template(template_type,interface_dict)
                    interface_list.append(interface_output)
                    print(v1,v2,v3)
        return interface_list

    def ipadd_loopback(self,template_type = "ipadd.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_input\\interface_id_prod_loopback.csv")
        results = pd.merge(df, df1, how='left', on=["HOSTNAME", "HOSTNAME"])
        for index,row in results.iterrows():
            if row['results__name'] == "Loopback0":
                for i in range(2):
                    if i == 0:
                        v1 = row['HOSTNAME'].strip()
                        v2 = row['results__name'].strip()
                        v3 = "default loopback"
                        v4 = row['IPV4_LOOPBACK0_ADDRESS'].strip() + "/32"
                        v5 = row['results__id']
                        ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4': v4, 'v5': v5}
                        ipadd_output = self.template(template_type, ipadd_dict)
                        ipadd_list.append(ipadd_output)
                    if i == 1:
                        v1 = row['HOSTNAME'].strip()
                        v2 = row['results__name'].strip()
                        v3 = "default loopback"
                        v4 = row['IPV6_LOOPBACK0_ADDRESS'].strip() + "/128"
                        v5 = row['results__id']
                        ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4': v4, 'v5': v5}
                        ipadd_output = self.template(template_type, ipadd_dict)
                        ipadd_list.append(ipadd_output)
            if row['results__name'] == "Loopback1":
                for i in range(2):
                    if i == 0:
                        v1 = row['HOSTNAME'].strip()
                        v2 = row['results__name'].strip()
                        v3 = "default loopback"
                        v4 = row['IPV4_MANAGEMENT_IP'].strip() + "/32"
                        v5 = row['results__id']
                        ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4': v4, 'v5': v5}
                        ipadd_output = self.template(template_type, ipadd_dict)
                        ipadd_list.append(ipadd_output)
                    if i == 1:
                        v1 = row['HOSTNAME'].strip()
                        v2 = row['results__name'].strip()
                        v3 = "default loopback"
                        v4 = row['IPV6_MANAGEMENT_IP'].strip() + "/128"
                        v5 = row['results__id']
                        ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4': v4, 'v5': v5}
                        ipadd_output = self.template(template_type, ipadd_dict)
                        ipadd_list.append(ipadd_output)
        return ipadd_list

    def phy_int(self,template_type = "physical.j2"):
        ipadd_dict = {}
        phy_be_df = pd.read_csv("data_input\\service_discovery_show_run_interface_bundle.csv")
        phy_l3_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l3vpn.csv")
        phy_l2_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l2vpn.csv")
        phy_be_df["bundle_id"] = "Bundle-Ether" + phy_be_df["bundle_id"].astype(str)
        phy_be_df["description"] = " "
        phy_be_df = phy_be_df[["hostname","interface","description","bundle_id"]]
        phy_l3_df_ = phy_l3_df[~phy_l3_df.interface.str.contains("Loopback")]
        phy_l3_df__ = phy_l3_df_[~phy_l3_df_.interface.str.contains("Bundle-Ether")]
        phy_l3_df__["bundle_id"] = " "
        phy_l3_df__ = phy_l3_df__[["hostname","interface","description","bundle_id"]]
        phy_l2_df_ = phy_l2_df[~phy_l2_df.interface.str.contains("Bundle-Ether")]
        phy_l2_df_["bundle_id"] = " "
        phy_l2_df_ = phy_l2_df_[["hostname", "interface", "description", "bundle_id"]]
        results = pd.concat([phy_be_df,phy_l3_df__,phy_l2_df_], ignore_index=True)
        results.to_csv("data_output/physical.csv", index=False)
        print(results.head(100))
        for index, row in results.iterrows():
            v1 = row['hostname']
            v2 = row['interface']
            v3 = row['description']
            v4 = row['bundle_id']
            if v4 == " ":
                template_type = "physical_only.j2"
            if "BVI" in row["interface"]:
                v5 = 'lag'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4':v4, 'v5': v5}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done with creating physical interface with be of " + v1)
            if "Hundred" in row["interface"]:
                v5 = '100gbase-x-qsfp28'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4':v4, 'v5': v5}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done with creating physical interface with be of " + v1)
            if "Ten" in row["interface"]:
                v5 = '10gbase-x-xfp'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4':v4, 'v5': v5}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done with creating physical interface with be of " + v1)
            if "Fort" in row["interface"]:
                v5 = '40gbase-x-qsfpp'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4':v4, 'v5': v5}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done with creating physical interface with be of " + v1)
            if "GigabitEthernet" in row["interface"]:
                v5 = '1000base-t'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'v4':v4, 'v5': v5}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done with creating physical interface with be of " + v1)
        return ipadd_list

    def shut_interfaces(self,template_type = "shut_interfaces.j2"):
        ipadd_dict ={}
        shut_int_df = pd.read_csv("data_input\\service_discovery_show_ip_interface_brief.csv")
        results = shut_int_df[~shut_int_df.status.str.contains("Up")]
        results.to_csv("data_output/physical_shut.csv", index=False)
        print(results.head(100))
        for index, row in results.iterrows():
            v1 = row["hostname"]
            v2 = row["intf"]
            if "Bundle-Ether" in row["intf"]:
                v3 = 'lag'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
            if "Hundred" in row["intf"]:
                v3 = '100gbase-x-qsfp28'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 + " physical " + v2)
            if "Ten" in row["intf"]:
                v3 = '10gbase-x-xfp'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 + " physical " + v2)
            if "Fort" in row["intf"]:
                v3 = '40gbase-x-qsfpp'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 + " physical " + v2)
            if "GigabitEthernet" in row["intf"]:
                v3 = '1000base-t'
                ipadd_dict = {'v1': v1, 'v2': v2, 'v3': v3, 'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 + " physical " + v2)
            #print("Done with creating physical shutdown interface of " + v1)
        return ipadd_list

    def be_int(self,template_type = "be.j2"):
        ipadd_dict = {}
        be_df = pd.read_csv("data_input\\service_discovery_show_run_interface_bundle.csv")
        be_df["bundle_id"] = "Bundle-Ether" + be_df["bundle_id"].astype(str)
        new_be_df = be_df.rename(columns={"bundle_id": "interface", "interface": "xx"})
        new_be_df["description"] = " "
        new_be_df = new_be_df[["hostname", "interface", "description"]]
        be_l2_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l2vpn.csv")
        be_l2_df_ = be_l2_df[~be_l2_df.interface.str.contains("Loopback")]
        be_l2_df__ = be_l2_df_[~be_l2_df_.interface.str.contains("TenGigE")]
        be_l2_df___ = be_l2_df__[~be_l2_df__.interface.str.contains("GigabitEthernet")]
        new_be_l2_df = be_l2_df___[~be_l2_df___.interface.str.contains("HundredGigE")]
        #df = df.dropna()
        new_be_l2_df = new_be_l2_df[["hostname","interface","description"]]
        be_l3_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l3vpn.csv")
        be_l3_df_ = be_l3_df[~be_l3_df.interface.str.contains("Loopback")]
        be_l3_df__ = be_l3_df_[~be_l3_df_.interface.str.contains("TenGigE")]
        be_l3_df___ = be_l3_df__[~be_l3_df__.interface.str.contains("GigabitEthernet")]
        new_be_l3_df = be_l3_df___[~be_l3_df___.interface.str.contains("HundredGigE")]
        #df1 = df1.dropna()
        new_be_l3_df = new_be_l3_df[["hostname", "interface", "description"]]
        results = pd.concat([new_be_df,new_be_l2_df,new_be_l3_df], ignore_index=True)
        results.to_csv("data_output/be.csv", index=False)
        #merge but just display the common outputs
        # results = pd.merge(df, df1, how='left', on=["hostname])
        # results = df1.merge(df[['HOSTNAME','SOURCE_BUNDLE_INTERFACE','SOURCE_IPV4_ADDRESS','SOURCE_IPV6_ADDRESS']])
        # results = results.dropna()
        for index,row in results.iterrows():
            # if row['results__name'] == "Loopback0" or row['results__name'] == "Loopback1":
            #     print("Skipping interface " + row["results__name"] + " of " + row["HOSTNAME"])
            #     continue
            v1 = row['hostname']
            v2 = row['interface']
            v3 = row['description']
            ipadd_dict = {'v1': v1, 'v2': v2,'v3': v3}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print ("Done with creating bundle-ether of " + v1)
        return ipadd_list

    def add_connection(self,template_type="connections.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_output\\synched.csv")
        results = df
        for index, row in results.iterrows():
            v1 = json.dumps([row["SOURCE_INTERFACE_ID"],row["HOSTNAME"]])
            v2 = json.dumps([row["TARGET_INTERFACE_ID"], row["TARGET_HOSTNAME"]])
            ipadd_dict = {'v1': v1, 'v2': v2}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
        print("Done adding connection between " + str(v1) + " and " + str(v2))
        return ipadd_list

    def rt(self,template_type="rt.j2"):
        ipadd_dict = {}
        rt_list = []
        rt_df = pd.read_csv("data_input\\service_discovery_show_run_vrf_details.csv")
        for index, row in rt_df.iterrows():
            #res = ast.literal_eval(ini_list)
            rt_list_import = ast.literal_eval(row["ipv4_rt_import"])
            rt_list_export = ast.literal_eval(row["ipv4_rt_export"])
            for rt in rt_list_import:
                if rt in rt_list:
                    continue
                else:
                    rt_list.append(rt)
            for rt in rt_list_export:
                if rt in rt_list:
                    continue
                else:
                    rt_list.append(rt)
        print(len(rt_list))
        for rt in rt_list:
            v1 = rt
            ipadd_dict = {'v1': v1}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with RT of " + row["hostname"])
        return ipadd_list

    def assign_rt(self,template_type="assign_rt.j2"):
        ipadd_dict = {}
        rt_df = pd.read_csv("data_input\\service_discovery_show_run_vrf_details.csv")
        #df.drop_duplicates(subset=['brand', 'style'], keep='last')
        rt_df_ = rt_df.drop_duplicates(subset=['vrf'],keep='last')
        for index, row in rt_df_.iterrows():
            v1 = row['vrf']
            v2 = json.dumps(ast.literal_eval(row["ipv4_rt_import"]))
            v3 = json.dumps(ast.literal_eval(row["ipv4_rt_export"]))
            ipadd_dict = {'v1': v1,'v2':v2,'v3':v3}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with RT of " + row["hostname"])
        return ipadd_list

    def vrf(self,template_type = "vrf.j2"):
        ipadd_dict = {}
        vrf_df = pd.read_csv("data_input\\service_discovery_show_ip_interface_brief.csv")
        vrf_df_ = vrf_df[~vrf_df.vrf.str.contains("default")]
        for index, row in vrf_df_.iterrows():
            v1 = row['vrf']
            ipadd_dict = {'v1': v1}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with vrf of " + row["hostname"])
        return ipadd_list

    def assign_vrf(self,template_type = "assign_vrf.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_input\\service_discovery_show_ip_interface_brief.csv")
        df_ = df[~df.status.str.contains("own")]
        df__ = df_[~df_.intf.str.contains("Loopback")]
        results = df__[~df__.vrf.str.contains("default")]
        for index, row in results.iterrows():
            v2 = row["vrf"]
            hostname = row["hostname"]
            interface = row["intf"]
            address = row["address"]
            ipadd_dict = {'address':address,'v2': v2, 'hostname': hostname, 'interface': interface}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with IP of " + " of " + v2)
        return ipadd_list

    def vlan(self,template_type = "vlan.j2"):
        ipadd_dict = {}
        phy_l3_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l3vpn.csv")
        phy_l2_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l2vpn.csv")
        phy_l3_df_ = phy_l3_df[~phy_l3_df.interface.str.contains("Loopback")]
        phy_l3_df__ = phy_l3_df_[~phy_l3_df_.interface.str.contains("BVI")]
        phy_l3_df__[["vlan"]] = phy_l3_df__[["vlan"]].fillna(0.0).astype(int)
        #phy_l3_df__ = phy_l3_df__.vlan.astype(int)
        phy_l3_df___ = phy_l3_df__[["hostname","interface","description","vlan"]]
        phy_l2_df_ = phy_l2_df[~phy_l2_df.interface.str.contains("Loopback")]
        phy_l2_df_[["vlan"]] = phy_l2_df_[["vlan"]].fillna(0.0).astype(int)
        #phy_l2_df_ = phy_l2_df_.vlan.astype(int)
        phy_l2_df__ = phy_l2_df_[["hostname", "interface", "description", "vlan"]]
        results = pd.concat([phy_l3_df___,phy_l2_df__], ignore_index=True)
        #rt_df_ = rt_df.drop_duplicates(subset=['vrf'], keep='last')
        results_new = results.drop_duplicates(subset=["vlan"])
        results_new.to_csv("data_output/assign_vlan.csv", index=False)
        for index, row in results_new.iterrows():
            v1 = row["vlan"]
            v2 = str(row["vlan"])
            ipadd_dict = {'v1': v1,'v2':v2}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with vlan of " + v2 + " of " + row["hostname"])
        return ipadd_list

    def assign_vlan(self,template_type="assign_vlan.j2"):
        ipadd_dict = {}
        phy_l3_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l3vpn.csv")
        phy_l2_df = pd.read_csv("data_input\\service_discovery_show_run_interface_l2vpn.csv")
        phy_l3_df_ = phy_l3_df[~phy_l3_df.interface.str.contains("Loopback")]
        phy_l3_df__ = phy_l3_df_[~phy_l3_df_.interface.str.contains("BVI")]
        phy_l3_df__[["vlan"]] = phy_l3_df__[["vlan"]].fillna(0.0).astype(int)
        #phy_l3_df__ = phy_l3_df__.vlan.astype(int)
        phy_l3_df___ = phy_l3_df__[["hostname","interface","description","vlan"]]
        phy_l2_df_ = phy_l2_df[~phy_l2_df.interface.str.contains("Loopback")]
        phy_l2_df_[["vlan"]] = phy_l2_df_[["vlan"]].fillna(0.0).astype(int)
        #phy_l2_df_ = phy_l2_df_.vlan.astype(int)
        phy_l2_df__ = phy_l2_df_[["hostname", "interface", "description", "vlan"]]
        results = pd.concat([phy_l3_df___,phy_l2_df__], ignore_index=True)
        results.to_csv("data_output/assign_vlan.csv", index=False)
        print(results.head(100))
        for index, row in results.iterrows():
            v1 = row["hostname"]
            v2 = row["interface"]
            v3 = str(row["vlan"])
            if "Bundle-Ether" in row["interface"] and "." in row["interface"]:
                type = 'lag'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3,'type':type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 + " bundle " + v2)
            if "Hundred" in row["interface"] and "." in row["interface"]:
                type = '100gbase-x-qsfp28'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3,'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 +" physical " + v2)
            if "Ten" in row["interface"] and "." in row["interface"]:
                type = '10gbase-x-xfp'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3,'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 +" physical " + v2)
            if "Fort" in row["interface"] and "." in row["interface"]:
                type = '40gbase-x-qsfpp'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3,'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 +" physical " + v2)
            if "GigabitEthernet" in row["interface"] and "." in row["interface"]:
                type = '1000base-t'
                ipadd_dict = {'v1': v1, 'v2': v2,'v3':v3,'type': type}
                ipadd_output = self.template(template_type, ipadd_dict)
                ipadd_list.append(ipadd_output)
                print("Done assigning vlan of " + v1 +" physical " + v2)
        return ipadd_list

    def ipadd_be(self,template_type = "ip_add_be.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_input\\service_discovery_show_run_interface_ip_address.csv")
        #df1 = pd.read_csv("data_input\\service_discovery_show_ip_interface_brief.csv")
        results = df
        results.to_csv("data_output/vrf.csv", index=False)
        # df1 = df1.dropna()
        #merge but just display the common outputs
        #results = pd.merge(df_, df1_, how='left', on=["hostname"])
        #results = df1.merge(df[['HOSTNAME','SOURCE_BUNDLE_INTERFACE','SOURCE_IPV4_ADDRESS','SOURCE_IPV6_ADDRESS']])
        #results = df
        for index,row in results.iterrows():
            # if row['results__name'] == "Loopback0" or row['results__name'] == "Loopback1":
            #     print("Skipping interface " + row["results__name"] + " of " + row["HOSTNAME"])
            #     continue
            # for i in range(2):
            #     if i == 0:
            # v1 = row['HOSTNAME']
            # v2 = row['SOURCE_BUNDLE_INTERFACE']
            # v4 = row['SOURCE_IPV4_ADDRESS']
            # v5 = bundle_id
            # ipadd_dict = {'v1': v1, 'v2': v2,'v4': v4, 'v5': v5}
            # ipadd_output = self.template(template_type, ipadd_dict)
            # ipadd_list.append(ipadd_output)
            # print ("Done with IPV4 of " + v1 + " of " + v2)
        # if i == 1:
            if "/" in row['address']:
                v4 = row['address']
            else:
                cidr = row['address']
                cidr = cidr.split(" ")
                cidr_ = IPAddress(cidr[1]).netmask_bits()
                cidr[1] = str(cidr_)
                v4 = "/".join(cidr)
            v1 = row['hostname']
            v2 = row['interface']
            ipadd_dict = {'v1': v1, 'v2': v2,'v4': v4}
            ipadd_output = self.template(template_type, ipadd_dict)
            ipadd_list.append(ipadd_output)
            print("Done with IP of " + v1 + " of " + v2)
        return ipadd_list




