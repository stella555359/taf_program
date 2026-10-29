# Generated with TL configuration generator at 2022-09-13_13:17:23

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
from taf.config.testline.pdu import PduPort, FPFH, HPE
import os
import yaml

# ------------------------POWER_BREAKERS-------------------------

_pdu_gnb = FPFH(
    addr="FPFH-HD06-46-P09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[5],
)
_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}
_pdu_gnb_ru = HPE(
    addr="hd06.mgt.ska-lab.nsn-rdnet.net",
    port_numbers=[9,10,11,18,19,20,21,22,23],
    snmp_user=_snmp_user,
)
# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.140.36/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.140.36/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
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
        addr="7-7-UTE5GCLOUDT9SK036.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_gnb_instance_id = 78336
_gnb_global_bts_id = 78336

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="10.84.140.36",
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

gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1220208444",
    product_code="475266A.103",
    slot_id=SlotId.B1
    )

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    pdu_port=PduPort(pdu=_pdu_gnb, port_no=5),
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH204361413",
    mac_addr="78:f9:b4:7d:b2:83",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
)

_airscale_gnb = Airscale(
    common_units=[gnb_common_unit_0],
    product_code="473098A"
    )

_ru_1 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH183002050",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[23],
)

_ru_2 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH183100336",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[22],
)

_ru_3 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH183001954",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[21],
)

_ru_4 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH182101115",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[20],
)

_ru_5 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH191000883",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[11],
)

_ru_6 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH190500703",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[18],
)

_ru_7 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHG",
    serial_number="NH204500494",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[9],
)

_ru_8 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHG",
    serial_number="NH221300917",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[10],
)

_ru_9 = RU(
    ru_hw_group="ASiR-HUB",
    radio_type="APHA",
    serial_number="NH182101061",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[19],
)

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9],
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

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],

    test_pcs=[_test_pc_gnb],

)

__all__ = ["tl"]
