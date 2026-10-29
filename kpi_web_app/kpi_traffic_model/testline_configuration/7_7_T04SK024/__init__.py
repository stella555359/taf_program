# Generated with TL configuration generator at 2024-01-04_08:21:46

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_gnb_pdu = FPFH(
    port_numbers=[1, 5],
    addr="fpfh-za10-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_enb_pdu = FPFH(
    port_numbers=[3, 4],
    addr="fpfh-zb10-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
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

_ru_pdu_0 = HPE(
    port_numbers=[12],
    addr="za10.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_ru_pdu_1 = HPE(
    port_numbers=[7, 10],
    addr="za09.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.148.24/23",
    routing_v4=RoutingInformation(gateway="10.84.149.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.20.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.24/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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
        addr="7-7-T04SK024.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77024
_gnb_global_bts_id = 77024

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

_gnb_ru_extension_unit_0 = RUExtension(
    radio_type="FA3WA",
    serial_number="YK212500177",
    product_code="475002A.101",
)

_gnb_ru_extension_unit_1 = RUExtension(
    radio_type="FA3UA",
    serial_number="YK202100166",
    product_code="475001A.101",
)

_gnb_radio_unit_0 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    serial_number="AH204101348",
    product_code="475166A.103",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=10),
    lmi=SerialOverTcp(uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.13.87"), port=2001)]),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AWEUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUC",
    serial_number="AH205100743",
    ru_extensions=[_gnb_ru_extension_unit_0],
    product_code="475168A.102",
    pdu_port=PduPort(pdu=_ru_pdu_0, port_no=12),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AWEUC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUC",
    serial_number="AH224401439",
    ru_extensions=[_gnb_ru_extension_unit_1],
    product_code="475168A.105",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=7),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="ARGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="ARGB",
    serial_number="L1254504254",
    product_code="476709A.101",
    pdu_port=PduPort(
        pdu=_gnb_pdu, port_no=1
    ),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233203427",
    product_code="475792A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.48",
    hardware_type="ABIO",
    hardware_version="A.107",
    serial_number="DH234324654",
    product_code="475266A.107",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_2],
)

_gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIA",
    hardware_version="A.107",
    serial_number="DH213393404",
    product_code="473096A.107",
    slot_id=SlotId.B6,
    rus=[_gnb_radio_unit_3],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1, _gnb_capacity_unit_2],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406323",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=5),
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

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.190.61/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.190.61/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T04SK061.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
    # connections are not defined because we do not want to perform yaft by
    # CommonAgent (eNb is usually shared between many gNBs)
)

_enb_instance_id = 77061
_enb_global_bts_id = 77061

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_0_radio_unit_0 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129",
        username="root",
        password="",
    ),
    radio_type="AHCA",
    serial_number="AS210105172",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_enb_pdu, port_no=3),
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="DH200295159",
    product_code="473096A.104",
    slot_id=SlotId.B4,
    rus=[_enb_0_radio_unit_0],
)

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="DH192551241",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_enb_pdu, port_no=4),
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="N/A",
)

_enb = RealEnb(
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_enb_0_airscale,
    oam_ip=_enb_oam_ip,
)

# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue = _set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_7_7_T04SK024",
)

__all__ = ["tl"]
