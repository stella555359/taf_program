import os
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, FPFH
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer, AppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.mcs import TopYoung
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAt
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "zhendong.Chen"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "zhendong.chen@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# test_pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.137", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##PB info
# FPFH-NPP A9232201001
_ru_pdu = FPFH(addr="10.57.176.210", port_numbers=[4])

# HBTE 6-6 PPB2003300003
_gnb_pdu = HBTE(addr="10.57.246.205", port_numbers=[6])

# 5GRU_1 for classicalBTS
##SN:1M222627864 - AQQY1   ToDo
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQY,
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.233.245"
)

# CU ToDo
_cu = CU(
    backhaul_site_oam_ip="10.57.233.245",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.245", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.245", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL617"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=617, global_bts_id=617)


# share with 7_5_UTE5G402T37178 : SN30022121789
_topyoung_mcs = TopYoung(
    ip_addr="10.57.230.247",
    port=28888,
    mcs_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="MCS2350A2-64B32-E6",
    version="",
)


# CI_Detail_UE_Type='Qualcomm CPE DX65'
_at_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.51",
    user="cmw_sg4",
    password="Zvmsg04_159357!",
    bind_interface_ip="10.57.163.51",
    expected_prompt="\$",
    binary_path="/home/cmw_sg4/taf_debug/iperf",
    ports=[53320, 54320],
)

_at_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_at_appserver_1,
    interval=1,
    binary_path="/cygdrive/c/Tools/",
    interface_name="Ethernet 2",
    server_close_delay=50,
    version=2,
    dt_from_uepc=True,
)

_at_1 = TafUeAt(
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    com_port="18",
    serial_number="36c74c83",
    ue_pc_address="10.57.150.199",
    ue_pc_login="mn5gran",
    ue_pc_password="nokia123@",
    ue_pc_expected_prompt="~",
    data_transfer=[_at_data_transfer_1],
    phone_number="",
    imei="",
    imsi="",
    capabilities=["REAL_QUALCOMM_UE1", "qualcomm"],
)

_at_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.51",
    user="cmw_sg4",
    password="Zvmsg04_159357!",
    bind_interface_ip="10.57.163.51",
    expected_prompt="\$",
    binary_path="/home/cmw_sg4/taf_debug/iperf",
    ports=[53700, 54700],
)

_at_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_at_appserver_2,
    interval=1,
    binary_path="/cygdrive/c/Tools/",
    interface_name="Ethernet 4",
    server_close_delay=50,
    version=2,
    dt_from_uepc=True,
)

_at_2 = TafUeAt(
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    com_port="14",
    serial_number="36da1f99",
    ue_pc_address="10.57.150.199",
    ue_pc_login="mn5gran",
    ue_pc_password="nokia123@",
    ue_pc_expected_prompt="~",
    data_transfer=[_at_data_transfer_2],
    phone_number="",
    imei="",
    imsi="",
    capabilities=["REAL_QUALCOMM2", "qualcomm"],
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_at_1, _at_2]
)
