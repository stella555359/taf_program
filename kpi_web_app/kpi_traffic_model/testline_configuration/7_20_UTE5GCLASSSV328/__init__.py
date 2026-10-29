# ##########################################################################################
#
#    7_20_UTE5GCLASSSV328  -  IV_PS_328  -  CV328
#
#    2023-12-17 22:23:49.033457:
#    __init__.py generator (version 2.0 of 02/12/2023).
#
# ##########################################################################################

__maintainer__ = "A NEZROUK"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "Abderrahmane.nezrouk@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
    IperfDataTransferIperfOptions,
)
from taf.config.testline.testpc import Connection, TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, FPFH, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android
from collections import OrderedDict
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.ue import PluginAndroidClassType

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["INIT_CONFIG_FILE_PATH"] = cfg_dir
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(cfg_dir, "ue_config.yaml")

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(
    addr="10.0.117.83", login="admin", password="admin", port_numbers=[2]
)
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.157", login="admin", password="admin", port_numbers=[1]
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.158", login="admin", password="admin", port_numbers=[1]
)
_ru3_pdu_gnb = FPFH(
    addr="10.0.117.138", login="admin", password="admin", port_numbers=[1]
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="L1202707617",
)
_rmod_gnb_3 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="L1204110687",
)
_rmod_gnb_2 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="L1204110688",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_2, _rmod_gnb_1, _rmod_gnb_3],
    serial_number="L1184210532",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIK",
    hardware_version="474021A.101",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        password="oZPS0POrRieRtu",
        port=22,
        username="toor4nsn",
    ),
    pdu_port=_du1_pdu_gnb.pdu_ports[2],
    serial_number="L1190102331",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23383, instance_id=328)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.49.161",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.161", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.161", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.15.146/29", vlan_id="4001"),
    x2c=NetworkAddress(v4="None"),
    x2u=NetworkAddress(v4="None"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23383, instance_id=328)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(
            device=_gnb_sbts_1.dus[0].airscale.common_units[0],
            interface="eth1",
            interface_type="lmp",
        ),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.150", password="uteUTE!", port=22, username="ute"
    ),
)
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.38.206", username="localuser", password="10c@1user"
    )
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb]

# iperf core network side
# ssh
_ue_host_iperf_ssh = SshServiceDetails(
    # addr="10.14.42.140", username="ftp", password="ftp"
    addr="10.0.106.248",
    username="ran5g",
    password="nokia2018",
)

_iperf_core_network_ssh = SshServiceDetails(
    addr="10.0.106.248",
    username="ran5g",
    password="nokia2018",
)

_ue_iperf_options = IperfDataTransferIperfOptions(
    packet="1300",
    buffer="8M",
    qci={1: 34000, 2: 34034},
    output_file="/tmp/iperf.txt",
)

# UL ports (UL traffic : port 33203 for first UE)
_appserver_ssh = AppServer(
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_iperf_core_network_ssh,
        network_interface_address="10.11.70.155",
        iperf_path=None,
        iperf_options=_ue_iperf_options,
        port="33203",
    )
)

_ue1_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.60.2.12",
    iperf_options=_ue_iperf_options,
)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.116.133", username="cv5g2_5", password="M!k@el5G", port=9090
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Capa_UE_1"],
    serial_number="5662c822",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_ue1_host_iperf_details,
    serial_com=8,
    diag_com=9,
    class_name=PluginAndroidClassType.at_cmd,
)

_ue2_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_iperf_ssh,
    network_interface_address="172.60.2.41",
    iperf_options=_ue_iperf_options,
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.97.203", username="cv5g2_5", password="M!k@el5G", port=9090
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Capa_UE_2"],
    serial_number="7b782800",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_ue2_host_iperf_details,
    serial_com=7,
    diag_com=3,
    class_name=PluginAndroidClassType.at_cmd,
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIK_ABIL_3xAEHC_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver_ssh,
    ues=[_ue1, _ue2],
)
