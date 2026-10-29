# Generated with TL configuration generator at 2022-06-20_22:19:27

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId, TRSInterfaces
from taf.config.testline.pdu import PduPort, FPFH
import os
import yaml


# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip = NetworkAddress(
    v4="10.84.190.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.20.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.148.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.20.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.148.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.20.85/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK085.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_gnb_instance_id = 77085
_gnb_global_bts_id = 77085

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_f1m_ip,
    f1c=_gnb_f1c_ip,
    f1u=_gnb_f1u_ip,
    x2c=_gnb_x2c_ip,
    x2u=_gnb_x2u_ip,
    s1c=_gnb_s1c_ip,
    s1u=_gnb_s1u_ip,
    xnc=_gnb_xnc_ip,
    xnu=_gnb_xnu_ip,
    ngc=_gnb_ngc_ip,
    ngu=_gnb_ngu_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_pdu1 = FPFH(
    port_numbers=[6],
    addr="10.255.13.33",
    login="admin",
    password="admin",
)

_pdu_ru1 = FPFH(
    port_numbers=[4],
    addr="10.255.13.33",
    login="admin",
    password="admin",

)

_pdu_ru2 = FPFH(
    port_numbers=[5],
    addr="10.255.13.17",
    login="admin",
    password="admin",
)

_pdu_ru3 = FPFH(
    port_numbers=[1],
    addr="10.255.13.33",
    login="admin",
    password="admin",
)

_pdu_ru4 = FPFH(
    port_numbers=[5],
    addr="10.255.13.33",
    login="admin",
    password="admin",
)

_pdu_ru5 = FPFH(
    port_numbers=[6],
    addr="10.255.13.17",
    login="admin",
    password="admin",
)

_pdu_ru6 = FPFH(
    port_numbers=[2],
    addr="10.255.13.33",
    login="admin",
    password="admin",
)

_gnb_capacity_unit = CapacityUnit(addr="192.168.253.24")

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit],
    hardware_type="ASOE",
    pdu_port=_pdu1.pdu_ports[6],
    hardware_version="A.102",
    serial_number="EA220250499",
    mac_addr="60:8f:a4:5f:b9:9",
    trs_connections=[],
    slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
     ru_hw_group="AHPB",
     pdu_port=_pdu_ru1.pdu_ports[4],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHPB",
     serial_number="K9200910377",
     product_code="474119A.101",
)

gnb_radio_unit_1 = RU(
     ru_hw_group="AHEB",
     pdu_port=_pdu_ru2.pdu_ports[5],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA220657597",
     product_code="473484A.101",
)

gnb_radio_unit_2 = RU(
     ru_hw_group="AHEB",
     pdu_port=_pdu_ru3.pdu_ports[1],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA220657592",
     product_code="473484A.101",
)

gnb_radio_unit_3 = RU(
     ru_hw_group="AHPB",
     pdu_port=_pdu_ru4.pdu_ports[5],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHPB",
     serial_number="K9200910586",
     product_code="474119A.101",
)

gnb_radio_unit_4 = RU(
     ru_hw_group="AHEB",
     pdu_port=_pdu_ru5.pdu_ports[6],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA220657596",
     product_code="473484A.101",
)

gnb_radio_unit_5 = RU(
     ru_hw_group="ARPA",
     pdu_port=_pdu_ru6.pdu_ports[2],
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="ARPA",
     serial_number="AS215107003",
     product_code="474802A.101",
)

_airscale_gnb = Airscale(
    common_units=[gnb_common_unit_0],
    product_code="N/A"
    )

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1, gnb_radio_unit_2, gnb_radio_unit_3, gnb_radio_unit_4, gnb_radio_unit_5],
    oam_ip=_gnb_oam_ip,
    f1_m_ip_addr=_gnb_f1m_ip,
    f1_c_ip_addr=_gnb_f1c_ip,
    f1_u_ip_addr=_gnb_f1u_ip,
    f1_m_cu=_gnb_f1m_ip,
    f1_c_cu=_gnb_f1c_ip,
    f1_u_cu=_gnb_f1u_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
    )

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)


# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASOE_AHEBx3_AHPBx2_ARPA",

)

__all__ = ["tl"]
