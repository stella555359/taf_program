# Generated with TL configuration generator at 2025-08-11_11:01:29

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
from taf.config.testline.attenuator import RadioRack
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
import os
import yaml

# ------------------------------UE---------------------------------
def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_attenuator = RadioRack(
    ip_addr="10.253.166.15", port=50000, attenuation_port_numbers=range(1, 33)
)

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1],
    addr="FPFH-GH10-46-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",
}

_ru_pdu = HPE(
    port_numbers=[2, 3, 4, 5, 6, 7, 9, 10, 11, 23],
    addr="gh10.mgt.krk-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT101.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 75101
_gnb_0_global_bts_id = 75101

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
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
    v4="10.83.252.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=541,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.253.212.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=542,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.253.212.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=542,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.83.182.101/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
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
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH230600516",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=5
    ),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH210200282",
    product_code="475295A.101S",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=10
    ),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH214300685",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=7
    ),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH211300666",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=4
    ),
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH225300524",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=9
    ),
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH210200274",
    product_code="475295A.101S",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=2
    ),
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH204500531",
    product_code="475295A.X21B",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=3
    ),
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHA",
    serial_number="NH191503369",
    product_code="474657A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=23
    ),
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH225300526",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=6
    ),
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH210300341",
    product_code="475295A.101S",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=11
    ),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.102",
    serial_number="L1213010175",
    product_code="474824A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_6, _gnb_0_radio_unit_8, _gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1184208621",
    product_code="474020A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_7],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1214600693",
    mac_addr="00:77:e4:a1:a3:0",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=1
    ),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="473098A",
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

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    attenuators=[_attenuator],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_9xAPHG_11xAWHGEQH"
)

__all__ = ["tl"]