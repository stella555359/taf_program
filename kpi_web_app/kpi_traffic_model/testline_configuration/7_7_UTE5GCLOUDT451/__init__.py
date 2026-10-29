__maintainer__ = "Dominik Wieczorek"
__owner_email__ = "dominik.wieczorek@nokia.com"
__team__ = "MN RAN Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"

import os

import yaml

from taf.config.testline.airscale import (
    Airscale, CapacityUnit, CommonUnit, SlotId
)
from taf.config.testline.connection_details import (
    HttpConnectionDetails, SshServiceDetails
)
from taf.config.testline.gnb import CU, DU, ClassicalBts
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress, RoutingInformation
)
from taf.config.testline.pdu import FPFH, HPE, PduPort
from taf.config.testline.radio import RU
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import Connection, TestPc


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[
        3,  # SMOD ASIL
        5,  # MicroRRH AWHHF
    ],
    addr="fpfh-gf01-46-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_hpe_web_user = {  # used for logging in via web browser
    "login": "user-lab0",
    "password": "NokiaBts2003",
}

_ru_pdu = HPE(
    port_numbers=[
        3,   # APHG SN: NH225300610 from BBMOD SN: DH215140065
        14,  # APHG SN: NH221300838 from BBMOD SN: DH215140064
        18,  # APHA SN: NH190500080 from BBMOD SN: DH215140064
    ],
    addr="ga23.mgt.krk-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.183.201/24",
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
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.83.183.201/24",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT451.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_instance_id = 75451
_gnb_global_bts_id = 75451

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
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AWHHF",
    serial_number="EB2050R0907",
    product_code="475181A.103",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=5),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300610",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=3),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH221300838",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=14),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHA",
    serial_number="NH190500080",
    product_code="474657A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=18),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH215140064",
    product_code="475266A.103",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_2, _gnb_radio_unit_3],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH215140065",
    product_code="475266A.103",
    slot_id=SlotId.B5,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1202703533",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="473098A",
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

# ------------------------TL_CONFIGURATION------------------------

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    ues=[_ue_config],
    pdus=[_bts_pdu, _ru_pdu],
)

__all__ = ["tl"]

