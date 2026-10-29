# Generated with TL configuration generator at 2024-05-17_06:46:16

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_gnb_pdu = FPFH(
    port_numbers=[1],
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
    port_numbers=[3, 12],
    addr="za10.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_ru_pdu_1 = HPE(
    port_numbers=[10],
    addr="za09.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK081.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 77081
_gnb_0_global_bts_id = 77081

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.190.81/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.190.81/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.148.81/23",
    routing_v4=RoutingInformation(gateway="10.84.149.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.20.81/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.22.81/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
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

_gnb_0_ru_extension_unit_0 = RUExtension(
    radio_type="FA3UA",
    serial_number="AH211820008",
    product_code="475001A.102",
)

_gnb_0_ru_extension_unit_1 = RUExtension(
    radio_type="FA3UA",
    serial_number="AH205000240",
    product_code="475001A.102",
)

_gnb_0_ru_extension_unit_2 = RUExtension(
    radio_type="FA3UA",
    serial_number="AH211720196",
    product_code="475001A.102",
)

_gnb_0_ru_extension_unit_3 = RUExtension(
    radio_type="FA3UA",
    serial_number="AH211820013",
    product_code="475001A.102",
)

_gnb_0_ru_extension_unit_4 = RUExtension(
    radio_type="FA3UA",
    serial_number="K202100133",
    product_code="475001A.101",
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    serial_number="AH204101348",
    ru_extensions=[_gnb_0_ru_extension_unit_2],
    product_code="475166A.103",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=10),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    serial_number="AH204101348",
    ru_extensions=[_gnb_0_ru_extension_unit_1, _gnb_0_ru_extension_unit_4],
    product_code="475166A.103",
    pdu_port=PduPort(pdu=_ru_pdu_0, port_no=12),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ=",
    ),
    radio_type="AWEUA",
    serial_number="AH204101349",
    ru_extensions=[_gnb_0_ru_extension_unit_0, _gnb_0_ru_extension_unit_3],
    product_code="475166A.103",
    pdu_port=PduPort(pdu=_ru_pdu_0, port_no=3),
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOF",
    hardware_version="A.101",
    serial_number="EA234550942",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=1),
)

_gnb_0_airscale = Airscale(
    core_units=[_gnb_0_core_unit_0],
    product_code="N/A",
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
        device=_gnb_0.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK061.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_0_instance_id = 77061
_enb_0_global_bts_id = 77061

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.190.61/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.190.61/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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

_enb_0 = RealEnb(
    x2_link_addr=_enb_0_oam_ip,
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
    system_module=_enb_0_airscale,
    oam_ip=_enb_0_oam_ip,
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
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_NSA_ASOF_3xAWEUA_FA3UA",
)

__all__ = ["tl"]
