__maintainer__ = "QT WRO"
__team__ = "MN RAN RD T&V OTA&CI QT1"
__email__ = "I_AM_QT@internal.nsn.com"
__owner_email__ = "I_AM_QT@internal.nsn.com"


import os
from taf.config.testline import RU, TafUeDataTransferProtocol
from taf.config.testline.airscale import Airscale, CommonUnit
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.connection_details import (
    HttpConnectionDetails,
    IperfDataTransferDetails,
    SshServiceDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts, DU
from taf.config.testline.pdu import Gude, PduPort
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import TafUeAndroid


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.239.58", username="ute", password="UTE.debian12"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.42.239.58", username="ute", password="UTE.debian12"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.44.184.204",
)

_appserver = AppServer(_iperf_details_on_appserver)

_appserver_taf_ue_WG = TafUeAppServer(app_server_name="wg-srn-iperf-728",
    address="10.44.184.246",
    user="qt5g",
    password="5Gqtmoth!",
    bind_interface_ip="10.44.184.246",
    expected_prompt="qt5g@wg-srn-iperf-728")

_data_transfer_iperf_WG = TafUeDataTransferProtocol(protocol_name="iperf",
    app_server=_appserver_taf_ue_WG,
    interval=1)

_cu = CU(
    backhaul_site_oam_ip="10.42.6.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.42.6.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.42.6.196", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_snmp_user_data=dict(
    userName="administrator",
    authKey="password",
    privKey="password",
    authProtocol="SHA1",
    privProtocol="AES-128",
)

_du_pdu = Gude(
    addr="10.44.71.24",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8221-1",
    snmp_user=_snmp_user_data,
)

_du_pdu_port = PduPort(pdu=_du_pdu, port_no=2)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[None],
    pdu_port=_du_pdu_port,
)

_airscale = Airscale(common_units=[_du_common_unit])

_ru_pdu = Gude(
    addr="10.44.71.24",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8221-1",
    snmp_user=_snmp_user_data,
)

_ru_pdu_port = PduPort(pdu=_ru_pdu, port_no=3)

_ru = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.128", username="root", password=""
    ),
    pdu_port=_ru_pdu_port,
)

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="192.168.255.129")

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_android_4G = TafUeAndroid(
    serial_number="91504f2b",
    capabilities=["_4G"],
    ue_pc_address="10.42.156.136",
    data_transfer=[_data_transfer_iperf_WG],
    ssh_connection_details=SshServiceDetails(
        addr="10.42.156.136", username="wro5gqt", password="5Gqtmoth"
    ),
    proxy_mngr_port=5000,
    imsi="android",
    qualcomm_prototype=False,
    voice_call_dialing_timeout="30",
    network_mode_switch_method="secretcode",
    airplane_mode_switcher_text="Off|On"
)

_android_4G.ue_type = "android"

tl = TestLine(
    test_pc=_test_pc,
    ues=[_android_4G],
    enbs=[_cbts],
    tl_cloud_topology="3115",
)

tl.target_traffic_4G = {
    "MIN_DL": "40",  # Mbits/sec
    "MIN_UL": "12",  # Mbits/sec
    "MAX_DL": "50",  # Mbits/sec
    "MAX_UL": "15",  # Mbits/sec
    "IPERF_DURATION": "70",  # seconds
    "cell_id_rf1": "13601547",
}

tl.custom = {
    "real_enb": "True",        # True if TL connected to LTE eNB
    "has_real_core": "True",    # True if TL not using EPCSim
}

tl.scf_variables = {
    # Sections IDs
    "MRBTS": "53131",
    "LNBTS": "53131",
    "BBMOD": "1",
    "LCELL": "11",
    "LNCEL": "1",
    "TRSNW": "1",

    # Site specific variables
    "_real_core": "true",
    "_gps": "false",
    "_top": "true",

    # MRBTS
    "btsName": "QT-ASIL-ABIP-4G-FDD-WRO-3115",
	
    # MRBTS/EQM/APEQM
    "location": "WRO",

    # MRBTS/EQM/APEQM/CABINET/SMOD
    "moduleLocation": "WG_L1-11_Rack1844",  # optional

    # MRBTS/EQM/HWTOP/CABLINK
    "firstEndpointPortId_BACKPLANE": "1",
    "firstEndpointPortId_OPT": "1",

    # MRBTS/LNBTS
    "mcc": "555",
    "mnc": "10",

    # MRBTS/LNBTS/LNMME
    "ipAddrPrim": "10.44.201.68",

    # MRBTS/LNBTS/LNCEL
    "lcrId": "11",
    "phyCellId": "11",
    "tac": "7160",

    # MRBTS/LNBTS/LNCEL/LNCEL_FDD
    "ulChBw": "10 MHz",
    "dlChBw": "10 MHz",
    "earfcnDL": "1800",
    "earfcnUL": "19800",

    # MRBTS/MNL/MNLENT/SYNC
    "btsSyncMode": "FreqSync",

    # MRBTS/MNL/MNLENT/SYNC/CLOCK
    "syncInputType": "TOPF",

    # MRBTS/MNL/MNLENT/SYNC/CLOCK/NTP
    "ntpServerIpAddrOrFqdnList": "10.42.162.252",

    # MRBTS/MNL/MNLENT/SYNC/CLOCK/TOP/TOPF
    "masterIpAddr": "10.42.161.252",

    # MRBTS/TNLSVC/TNL/ETHSVC/ETHIF/VLANIF
    "vlanId": "195",

    # MRBTS/TNLSVC/TNL/IPNO/IPRT
    "gateway": "10.42.6.193",

    # MRBTS/TNLSVC/TNL/IPNO/IPIF/IPADDRESSV4
    "localIpAddr": "10.42.6.196",
    "localIpPrefixLength": "27",
}

__all__ = ["tl"]
