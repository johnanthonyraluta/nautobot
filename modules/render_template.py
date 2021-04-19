import csv
import json
import requests
import ast
from jinja2 import Environment, FileSystemLoader
from data_output.region_list import region_list
import pandas as pd
import uuid

file_path = "C:\\Users\\jraluta\\nautobot\\"
device_list = []
roles_list = []
interface_list = []
ipadd_list = []

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
                # file_loader = FileSystemLoader(file_path + "templates")
                # env = Environment(loader=file_loader)
                # template = env.get_template("region.j2")
                # output = template.render(region_dict)
                #output = json.loads(output)
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
                roles_dict = {'v1':v1,'v2':v2,'v3':v3}
                roles_output = self.template(template_type,roles_dict)
                roles_list.append(roles_output)
        return roles_list

    def devices(self,template_type = "devices.j2"):
        device_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_output\\showplat_facts_pilot.csv")
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
            v10="_".join(v10_.split()).strip()
            device_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'v6':v6,'v7':v7,'v8':v8,\
                           'v9':v9,'v10':v10}
            device_output = self.template(template_type,device_dict)
            device_list.append(device_output)
        return device_list

    def patch_devices(self,template_type = "patch_devices.j2"):
        device_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_input\\interface_id_ver2.csv")
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

    def inventory(self,template_type = "inventory.j2"):
        inventory_dict = {}
        df = pd.read_csv("data_output\\showplat_facts_pilot.csv")
        df = df.dropna()
        df1 = pd.read_csv("data_input\\interface_id_ver4.csv")
        df1 = df1.dropna()
        #merge but just display the common outputs
        #results = pd.merge(df, df1, how='left', on=["SOURCE_BUNDLE_INTERFACE", "SOURCE_BUNDLE_INTERFACE"])
        results = df.merge(df1[['HOSTNAME','device/id']])
        results = results.dropna()
        results = results.drop_duplicates()
        #print(results)
        #print(resd)
        for index, row in results.iterrows():
            v1=row['device/id']
            v2=row['HOSTNAME']
            modules=row['MODULES']
            #v2 = v2_.replace("'",'"')
            modules = ast.literal_eval(modules)
            for module in modules:
                v4 = module['location'].strip()
                v3 = module['card_type'].strip()
                device_dict = {'v1':v1,'v2':v2,'v3':v3,'v4':v4}
                device_output = self.template(template_type,device_dict)
                device_list.append(device_output)
        return device_list


    def interfaces(self,template_type = "interface.j2"):
        interface_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        for index,row in df.iterrows():
            for i in range(2):
                v1 = row['HOSTNAME'].strip()
                my_uuid = str(uuid.uuid4())
                if i == 0:
                    v2 = i
                    v3 = "default loopback"
                    v4 = my_uuid
                    interface_dict = {'v1':v1,'v2':v2,'v3':v3,"v4":v4}
                    interface_output = self.template(template_type,interface_dict)
                    interface_list.append(interface_output)
                    print(v1,v2,v3,v4)
                if i == 1:
                    v2 = i
                    v3 = "network management loopback"
                    v4 = my_uuid
                    interface_dict = {'v1':v1,'v2':v2,'v3':v3,"v4":v4}
                    interface_output = self.template(template_type,interface_dict)
                    interface_list.append(interface_output)
                    print(v1,v2,v3,v4)
        return interface_list

    def ipadd_loopback(self,template_type = "ipadd.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_input\\site_info.csv")
        df1 = pd.read_csv("data_input\\interface_id_ver2.csv")
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

    def ipadd_be(self,template_type = "ip_add_be.j2"):
        ipadd_dict = {}
        df = pd.read_csv("data_input\\be_interface_ip.csv")
        df = df.dropna()
        df1 = pd.read_csv("data_input\\interface_id_ver4.csv")
        df1 = df1.dropna()
        #merge but just display the common outputs
        #results = pd.merge(df, df1, how='left', on=["SOURCE_BUNDLE_INTERFACE", "SOURCE_BUNDLE_INTERFACE"])
        results = df1.merge(df[['HOSTNAME','SOURCE_BUNDLE_INTERFACE','SOURCE_IPV4_ADDRESS','SOURCE_IPV6_ADDRESS']])
        results = results.dropna()
        print(results)
        for index,row in results.iterrows():
            # if row['results__name'] == "Loopback0" or row['results__name'] == "Loopback1":
            #     print("Skipping interface " + row["results__name"] + " of " + row["HOSTNAME"])
            #     continue
            for i in range(2):
                if i == 0:
                    v1 = row['HOSTNAME']
                    v2 = row['SOURCE_BUNDLE_INTERFACE']
                    v4 = row['SOURCE_IPV4_ADDRESS']
                    v5 = row['results__id']
                    ipadd_dict = {'v1': v1, 'v2': v2,'v4': v4, 'v5': v5}
                    ipadd_output = self.template(template_type, ipadd_dict)
                    ipadd_list.append(ipadd_output)
                    print ("Done with IPV4 of " + v1 + " of " + v2)
                if i == 1:
                    v1 = row['HOSTNAME']
                    v2 = row['SOURCE_BUNDLE_INTERFACE']
                    v4 = row['SOURCE_IPV6_ADDRESS']
                    v5 = row['results__id']
                    ipadd_dict = {'v1': v1, 'v2': v2,'v4': v4, 'v5': v5}
                    ipadd_output = self.template(template_type, ipadd_dict)
                    ipadd_list.append(ipadd_output)
                    print("Done with IPV6 of " + v1 + " of " + v2)
        return ipadd_list




