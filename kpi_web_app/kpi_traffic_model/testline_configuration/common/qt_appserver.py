import os
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeAt


appserver_WRO_01 =  ["10.45.168.53", "qt5g@wl-srn-server-1-idf34"]    #[IP Address, Expected prompt]
appserver_WRO_02 =  ["10.42.197.170", "qt5g@wl-srn-server-2-idf34"]    #[IP Address, Expected prompt]
appserver_WRO_03 =  ["10.42.249.116", "qt5g@wl-srn-server-3-1094"]    #[IP Address, Expected prompt]
appserver_WRO_04 =  ["10.44.184.246", "qt5g@wg-srn-iperf-728"]        #[IP Address, Expected prompt]
appserver_OULU_01 = ["10.35.102.96", "srn@iperfU39"]                  #[IP Address, Expected prompt]
appserver_WRO_user = "qt5g"
appserver_WRO_password = "5Gqtmoth!"
appserver_OULU_user = "srn"
appserver_OULU_password = "!!IperfUser@25!"


appserver_WRO = appserver_WRO_01
appserver_OULU = appserver_OULU_01


def appserver_qt(appserver_name):
    appserver_nr_list = globals()[appserver_name]
    if "WRO" in appserver_name:
        user = appserver_WRO_user
        password = appserver_WRO_password
    elif "OULU" in appserver_name:
        user = appserver_OULU_user
        password = appserver_OULU_password

    return TafUeAppServer(
        app_server_name = "APP_TAF_UE",
        address = appserver_nr_list[0],
        user = user,
        password = password,
        bind_interface_ip = appserver_nr_list[0],
        expected_prompt = appserver_nr_list[1]
    )
