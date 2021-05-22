import pandas as pd
from netaddr import IPAddress
from modules.sqlalchemy_connect import sqlalc_conn
import sys

# query_list = ["select * from cisco_tnt_c_tnt_show_cdp_neighbors_detail;"
#               "select * from cisco_tnt_c_tnt_show_run_interface_bundle;"
#               "select * from cisco_tnt_c_tnt_show_run_interface_ip_address;"]
def import_from_db():
    db_connection = sqlalc_conn()
    # if 'all' in site_name:
    neig_det_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_cdp_neighbors_detail", con=db_connection)
    int_bundle_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_run_interface_bundle", con=db_connection)
    run_ipadd_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_run_interface_ip_address", con=db_connection)
    l2vpn_int_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_run_interface_l2vpn", con=db_connection)
    l3vpn_int_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_run_interface_l3vpn", con=db_connection)
    show_ip_int_df = pd.read_sql("select * from cisco_tnt_c_tnt_show_ip_interface_brief", con=db_connection)
    # else:
    #     neig_det_df = pd.read_sql(f"select * from cisco_tnt_c_tnt_show_cdp_neighbors_detail where `hostname` like \
    #         '%%{site_name}%%'", con=db_connection)
    #     int_bundle_df = pd.read_sql(f"select * from cisco_tnt_c_tnt_show_run_interface_bundle where `hostname` like \
    #         '%%{site_name}%%'", con=db_connection)
    #     run_ipadd_df = pd.read_sql(f"select * from cisco_tnt_c_tnt_show_run_interface_ip_address where `hostname` like \
    #         '%%{site_name}%%'", con=db_connection)
    neig_det_df.to_csv("data_input/service_discovery_cdp_neigbors_detail.csv", index=False)
    int_bundle_df.to_csv("data_input/service_discovery_show_run_interface_bundle.csv", index=False)
    run_ipadd_df.to_csv("data_input/service_discovery_show_run_interface_ip_address.csv", index=False)
    l2vpn_int_df.to_csv("data_input/service_discovery_show_run_interface_l2vpn.csv", index=False)
    l3vpn_int_df.to_csv("data_input/service_discovery_show_run_interface_l3vpn.csv", index=False)
    show_ip_int_df.to_csv("data_input/service_discovery_show_ip_interface_brief.csv", index=False)
def sync_from_db(site_name):
    path = r"data_output\\synched.xlsx"
    cdp_df = pd.read_csv("data_input\\service_discovery_cdp_neigbors_detail.csv")
    ip_int_df = pd.read_csv("data_input\\service_discovery_show_run_interface_ip_address.csv")
    int_bundle_df = pd.read_csv("data_input\\service_discovery_show_run_interface_bundle.csv")
    sync_df__ = pd.merge(cdp_df.rename(columns={"hostname":"HOSTNAME","local_port":"SOURCE_INTERFACE_ID"}),int_bundle_df.\
                         rename(columns={"hostname":"HOSTNAME","interface":"SOURCE_INTERFACE_ID"}),how="inner", \
                         on=["HOSTNAME","SOURCE_INTERFACE_ID"])
    sync_df_ = pd.merge(sync_df__.rename(columns={"dest_host":"TARGET_HOSTNAME","remote_port":"TARGET_INTERFACE_ID",\
                        "bundle_id":"SOURCE_BUNDLE_INTERFACE"}),int_bundle_df.rename(columns={"hostname":"TARGET_HOSTNAME",\
                        "interface":"TARGET_INTERFACE_ID"}),how="inner", on=["TARGET_HOSTNAME","TARGET_INTERFACE_ID"])
    print(sync_df_.head(100))
    sync_df_["SOURCE_BUNDLE_INTERFACE"] = "Bundle-Ether" + sync_df_["SOURCE_BUNDLE_INTERFACE"].astype(str)
    sync_df_["bundle_id"] = "Bundle-Ether" + sync_df_["bundle_id"].astype(str)
    sync_df_.rename(columns = {"bundle_id":"TARGET_BUNDLE_INTERFACE"},inplace=True)
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
            cidr = sync_df_.loc[sync_df_["SOURCE_ADDRESS"] == ip, "SOURCE_ADDRESS"].iloc[0]
            cidr = cidr.split(" ")
            cidr_ = IPAddress(cidr[1]).netmask_bits()
            cidr[1] = str(cidr_)
            sync_df_.loc[sync_df_["SOURCE_ADDRESS"] == ip, ["SOURCE_ADDRESS"]] = "/".join(cidr)
            print("Done for SOURCE " + "/".join(cidr))
        except:
            continue

    for ipv6 in sync_df_["TARGET_ADDRESS"]:
        try:
            cidr = sync_df_.loc[sync_df_["TARGET_ADDRESS"] == ipv6, 'TARGET_ADDRESS'].iloc[0]
            cidr = cidr.split(" ")
            cidr_ = IPAddress(cidr[1]).netmask_bits()
            cidr[1] = str(cidr_)
            sync_df_.loc[sync_df_["TARGET_ADDRESS"] == ipv6, ['TARGET_ADDRESS']] = "/".join(cidr)
            print("Done for TARGET " + "/".join(cidr))
        except:
            continue

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
    if "all" in site_name:
        sync_df_.to_csv(f"data_output/synched.csv",index=False)
        print("Done saving " + f"data_output/synched.csv")
    else:
        indexNames = sync_df_[(sync_df_["HOSTNAME"] != site_name)].index
        sync_df_.drop(indexNames, inplace=True)
        sync_df_.to_csv(f"data_output/synched_{site_name}.csv", index=False)
        print("Done saving " + f"data_output/synched_{site_name}.csv")



def main():
    try:
       sys.argv[1]
    except:
       print("Please specify the hostname or all to sync all devices e.g. python sync_data.py all")
       sys.exit(1)
    site_name = sys.argv[1]
    import_from_db()
    sync_from_db(site_name)

if __name__ == '__main__':
    main()

