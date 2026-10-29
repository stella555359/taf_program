# Generated with TL configuration generator at 2023-12-11_08:22:52

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

# ------------------------------UE--------------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[3, 4],  # update port_no
    addr="fpfh-zc15-22-p01.p01-leg.ska-lab.nsn-rdnet.net",  # update address
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

_ru_pdu = HPE(
    port_numbers=[18, 19, 20, 21, 22],  # update port_no
    addr="zc15.mgt.ska-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.164.164/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.164.164/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.150.164/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.150.164/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.150.164/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
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

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK164.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 76164
_gnb_global_bts_id = 76164

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
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
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.128",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300289",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=21),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHA",
    serial_number="NH201800154",
    product_code="474657A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=18),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.130",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300331",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=19),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.10",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300263",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=22),
)

_gnb_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.131",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300327",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=20),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1212110996",
    product_code="475266A.103",
    slot_id=SlotId.B5,
    rus=[_gnb_radio_unit_3],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223610009",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2, _gnb_radio_unit_4],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH220447104",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
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

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.164.42/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.164.42/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK042.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
    # connections are not defined because we do not want to perform yaft by
    # CommonAgent (eNb is usually shared between many gNBs)
)

_enb_instance_id = 76042
_enb_global_bts_id = 76042

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH225300289",
    product_code="475295A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.130",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH225300327",
    product_code="475295A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_radio_unit_2 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.131",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type="APHA",
    serial_number="NH201800154",
    product_code="474657A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203290552",
    product_code="473096A.105",
    slot_id=SlotId.B1,
    rus=[_enb_radio_unit_0, _enb_radio_unit_1, _enb_radio_unit_2],
)

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="L1171401881",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_airscale_enb = Airscale(
    common_units=[_enb_common_unit_0],
    product_code="473098A",
)

_enb = RealEnb(
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb_main, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIR_ASIBR_ABIOB4_ABIOB5_APHA_4xAPHG_2xAHFHIA_4xAWHHIQB",
)

__all__ = ["tl"]
