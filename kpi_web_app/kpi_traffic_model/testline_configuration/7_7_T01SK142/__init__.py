# Generated with TL configuration generator at 2024-06-03_09:50:54

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
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote
from taf.config.testline.attenuator import RadioRack
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[2, 4, 5, 6],
    addr="FPFH-za15-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdus = FPFH(
    port_numbers=[1, 2],
    addr="FPFH-za16-46-P01.p01-leg.ska-lab.nsn-rdnet.net",
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

_ru_pdu_AWHQX = HPE(
    port_numbers=[13],
    addr="za15.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_ru_pdu_AWEUC = HPE(
    port_numbers=[3],
    addr="za02.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01SK142-1.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01SK142-2.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 76142
_gnb_0_global_bts_id = 76142

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0_secondary.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.164.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.164.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="10.255.6.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.6.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.8.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.150.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.255.6.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.150.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.255.8.142/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_0_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_0_oam_http_connection,
    f1m=_gnb_0_f1m_ip,
    f1c=_gnb_0_f1c_ip,
    f1u=_gnb_0_f1u_ip,
    x2c=_gnb_0_x2c_ip,
    x2u=_gnb_0_x2u_ip,
    s1c=_gnb_0_s1c_ip,
    s1u=_gnb_0_s1u_ip,
    xnc=_gnb_0_xnc_ip,
    xnu=_gnb_0_xnu_ip,
    ngc=_gnb_0_ngc_ip,
    ngu=_gnb_0_ngu_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AWEUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AWEUC",
    serial_number="AH211500032",
    product_code="475168A.104",
    pdu_port=PduPort(pdu=_ru_pdu_AWEUC, port_no=3),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHLOA",
    serial_number="BL2050G1SOF",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=5),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="cMAArChile_64T64R",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AEHC",
    serial_number="AH231800619",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdus, port_no=1),
    # lmi=SerialOverTcp(
    #     uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.10.121"), port=2001)]
    # ),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AWHQX",
    serial_number="EB2335R0681",
    product_code="475927A.101",
    pdu_port=PduPort(pdu=_ru_pdu_AWHQX, port_no=13),
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHFIB",
    serial_number="BL2031V0F46",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=6),
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AWHQN",
    serial_number="EB2244R1932",
    product_code="475701A.102",
    pdu_port=PduPort(pdu=_ru_pdus, port_no=2),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="EA193476705",
    product_code="474020A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.102",
    serial_number="L1213010189",
    product_code="474824A.102",
    slot_id=SlotId.B6,
    rus=[_gnb_0_radio_unit_5],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="root@fct-0a:~",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1233005544",
    product_code="476397A.102",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_4],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1240606966",
    product_code="475792A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_1],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1240606982",
    product_code="475792A.102",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_2],
)

_gnb_0_capacity_unit_5 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233803054",
    product_code="475792A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_3],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_3, _gnb_0_capacity_unit_4, _gnb_0_capacity_unit_5],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406233",
    mac_addr="",
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH223249833",
    mac_addr="",
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
    product_code="475773A.101",
)

_du_gnb_0 = DU(
    airscale=_gnb_0_airscale,
    oam_ip=_gnb_0_oam_ip,
    f1_m_ip_addr=_gnb_0_f1m_ip,
    f1_c_ip_addr=_gnb_0_f1c_ip,
    f1_u_ip_addr=_gnb_0_f1u_ip,
    f1_m_cu=_gnb_0_f1m_ip,
    f1_c_cu=_gnb_0_f1c_ip,
    f1_u_cu=_gnb_0_f1u_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_test_pc_gnb_0_secondary.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[1],
        interface="eth1",
        interface_type="lmp",
    )
]


# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# Attenuators
_attenuator1 = RadioRack(
    ip_addr="10.255.10.103", port=23, attenuation_port_numbers=range(1, 16)
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    attenuators=[_attenuator1],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_7_7_T01SK142",
)

__all__ = ["tl"]
