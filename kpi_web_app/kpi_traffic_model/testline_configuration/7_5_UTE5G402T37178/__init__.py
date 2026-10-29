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
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import TafUeFastmile

__maintainer__ = "Shifu Lan"  # TL owner name
__team__ = "I_MN_RAN_RD_VRF_HAZ_04_GMS <I_MN_RAN_RD_VRF_HAZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "shifu.lan@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# test_pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.96", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##PB info
# FPFH-NPP 6-6 WOTA08 U16-U24 A9232201001
_ru_pdu = FPFH(addr="10.68.87.114", port_numbers=[3])
# HBTE 6-6 WOTA09 U40 Left PPB2003300003
_gnb_pdu = HBTE(addr="10.68.87.106", port_numbers=[3])

# 5GRU for classicalBTS
##SN:1M202406692 - AEQZ
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQZ,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ASOE")


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASOE",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1, ], f1_m_ip_addr="10.68.89.6"
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.89.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.6", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.6",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.1/27"),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.6",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.1/27"),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.6",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.1/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL37178"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37178, global_bts_id=37178)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53371, 54471],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.159.48",
    root_password="cf7a863279f3",
    ue_manage_ip="10.71.213.145",
    serial_number="FSH204000046",
    data_transfer=[_fastmile_data_transfer_1],
    #ue_pc_port=9955,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53372, 54372],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
   protocol_name='iperf',
   app_server=_fastmile_appserver_2,
   interval=1,
   binary_path='iperf',
   version=2)

_fastmile_2= TafUeFastmile(
   ue_pc_address='10.57.159.48',
   root_password='678a8ec23cfb',
   ue_manage_ip='10.71.213.146',
   serial_number='FSH20400005F',
   data_transfer=[_fastmile_data_transfer_2],
   #ue_pc_port=9955,
   proxy_mngr_port=9955,
   ueproxy_force_release=True,
   capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    #ues=[_fastmile_1, _fastmile_2],
)
