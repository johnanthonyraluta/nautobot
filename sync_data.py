import pandas as pd
from netaddr import IPAddress

path = r"data_output\\synched.xlsx"
#writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
cdp_df= pd.read_csv('data_input\\service_discovery_cdp_neigbors_detail.csv')
ip_int_df = pd.read_csv('data_input\\service_discovery_show_run_interface_ip_address.csv')
int_bundle_df = pd.read_csv('data_input\\service_discovery_show_run_interface_bundle.csv')
sync_df__ = pd.merge(cdp_df.rename(columns={"hostname":"HOSTNAME","local_port":"SOURCE_INTERFACE_ID"}),int_bundle_df.\
                     rename(columns={"hostname":"HOSTNAME","interface":"SOURCE_INTERFACE_ID"}),how="inner", \
                     on=["HOSTNAME","SOURCE_INTERFACE_ID"])
sync_df_ = pd.merge(sync_df__.rename(columns={"dest_host":"TARGET_HOSTNAME","remote_port":"TARGET_INTERFACE_ID",\
                    "bundle_id":"SOURCE_BUNDLE_INTERFACE"}),int_bundle_df.rename(columns={"hostname":"TARGET_HOSTNAME",\
                    "interface":"TARGET_INTERFACE_ID"}),how="inner", on=["TARGET_HOSTNAME","TARGET_INTERFACE_ID"])
sync_df_["SOURCE_BUNDLE_INTERFACE"] = "Bundle-Ether" + sync_df_["SOURCE_BUNDLE_INTERFACE"].astype(str)
sync_df_["bundle_id"] = "Bundle-Ether" + sync_df_["bundle_id"].astype(str)
sync_df_.rename(columns={"bundle_id":"TARGET_BUNDLE_INTERFACE"},inplace=True)
sync_df_ = pd.merge(sync_df_,ip_int_df.rename(columns={"hostname":"HOSTNAME","interface":"SOURCE_BUNDLE_INTERFACE"}),\
                    how="left", on = ["HOSTNAME","SOURCE_BUNDLE_INTERFACE"])
sync_df_.rename(columns={"address":"SOURCE_ADDRESS"},inplace=True)
sync_df_ = pd.merge(sync_df_,ip_int_df.rename(columns={"hostname":"TARGET_HOSTNAME","interface":"TARGET_BUNDLE_INTERFACE"}),\
                    how="left", on = ["TARGET_HOSTNAME","TARGET_BUNDLE_INTERFACE"])
sync_df_.rename(columns={"address":"TARGET_ADDRESS"},inplace=True)
print(sync_df_.head(100))
sync_df_ = sync_df_[["timestamp_x","HOSTNAME","SOURCE_INTERFACE_ID","SOURCE_BUNDLE_INTERFACE","SOURCE_ADDRESS",\
                     "TARGET_HOSTNAME","TARGET_INTERFACE_ID","TARGET_BUNDLE_INTERFACE","TARGET_ADDRESS"]]
for ip in sync_df_["SOURCE_ADDRESS"]:
    try:
        cidr = sync_df_.loc[sync_df_["SOURCE_ADDRESS"] == ip, 'SOURCE_ADDRESS'].iloc[0]
        cidr = cidr.split(" ")
        cidr_ = IPAddress(cidr[1]).netmask_bits()
        cidr[1] = str(cidr_)
        sync_df_.loc[sync_df_["SOURCE_ADDRESS"] == ip, ['SOURCE_ADDRESS']] = "/".join(cidr)
        print("Done for SOURCE" + "/".join(cidr))
    except:
        continue

for ipv6 in sync_df_["TARGET_ADDRESS"]:
    try:
        cidr = sync_df_.loc[sync_df_["TARGET_ADDRESS"] == ipv6, 'TARGET_ADDRESS'].iloc[0]
        cidr = cidr.split(" ")
        cidr_ = IPAddress(cidr[1]).netmask_bits()
        cidr[1] = str(cidr_)
        sync_df_.loc[sync_df_["TARGET_ADDRESS"] == ipv6, ['TARGET_ADDRESS']] = "/".join(cidr)
        print("Done for TARGET" + "/".join(cidr))
    except:
        continue

# indexNames = ip_int[(ip_int['proto'] == 'Down')].index
# ip_int.drop(indexNames, inplace=True)
#if a['Names'].str.contains('Mel').any():
for i, row in sync_df_.iterrows():
    source = row["SOURCE_ADDRESS"]
    dest = row["TARGET_ADDRESS"]
    if "/30" in source and "/30" in dest:
        continue
    if "/127" in source and "/127" in dest:
        continue
    else:
        # df.drop(df[df['Age'] < 25].index, inplace = True)
        sync_df_.drop(sync_df_[(sync_df_["SOURCE_ADDRESS"]==source) & (sync_df_["TARGET_ADDRESS"]==dest)].index, \
                      inplace=True)
        print("Dropped " + source + " " + dest)
print(sync_df_.head(100))
#sync_df = sync_df_.rename(columns={"hostname":"HOSTNAME"})
sync_df_.to_csv("data_output/synched.csv",index=False)
print("Done saving to " + path)