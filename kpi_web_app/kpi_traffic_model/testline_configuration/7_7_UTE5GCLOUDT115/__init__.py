# Generated with TL configuration generator at 2023-11-03_10:40:43

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CoreUnit, CapacityUnit, SlotId, TRSInterfaces
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline.pdu import FPFH
import os
import yaml

# -------------------------PDUs-----------------------------------

_pdu_du = FPFH(
    addr="fpfh-gf02-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[4],
)

_pdu_ru = FPFH(
    addr="fpfh-gf02-25-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[2, 3, 4],
)

_pdu_4g = FPFH(
    addr="fpfh-gf02-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[3, 6],
)
# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.115/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.115/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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
    v4="10.83.252.115/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.253.212.115/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.253.214.115/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT115.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_gnb_instance_id = 75115
_gnb_global_bts_id = 75115

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection,
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

_gnb_radio_unit_0 = RU(
     ru_hw_group="AHEB",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA204156239",
     product_code="473484A.101",
     pdu_port=_pdu_ru.pdu_ports[4],
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="AHEB",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA204156259",
     product_code="473484A.101",
     pdu_port=_pdu_ru.pdu_ports[3],
)

_gnb_radio_unit_2 = RU(
     ru_hw_group="AHEB",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHEB",
     serial_number="EA204156242",
     product_code="473484A.101",
     pdu_port=_pdu_ru.pdu_ports[2],
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.Y16",
    serial_number="L1224710453",
    product_code="475792A.Y16",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1224211817",
    pdu_port=_pdu_du.pdu_ports[4],
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="473098A"
    )

_du_gnb = DU(
    airscale=_airscale_gnb,
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

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb.connections = [
    Connection(
        device=_gnb.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.83.182.29/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.83.253.254"),
    vlan_id=503,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.83.182.29/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.83.253.254"),
    vlan_id=503,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT029.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_enb_instance_id = 75029
_enb_global_bts_id = 75029

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_radio_unit_0 = RU(
     ru_hw_group="AHEGC",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129",
        username="root",
        password="umniedziala"),
     radio_type="AHEGC",
     serial_number="EA205050759",
     product_code="474914A.101",
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.106",
    serial_number="DH204991812",
    product_code="473096A.106",
    slot_id=SlotId.B1,
    rus=[_enb_radio_unit_0],
    )

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="EA202955936",
    mac_addr="",
    slot_id=SlotId.C1,
)

_airscale_enb = Airscale(
    common_units=[_enb_common_unit_0],
    product_code="473098A"
    )

_enb = RealEnb(
    rms=[_enb_radio_unit_0],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASILL_ABIPB1_3xAHEB",
)

__all__ = ["tl"]
