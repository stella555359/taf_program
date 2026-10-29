# Generated with TL configuration generator at 2024-07-12_17:37:15

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


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[3, 4],         # update port_no
    addr="fpfh-zc06-26-p01.p01-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[3],         # update port_no
    addr="zc06.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK136-1.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_0_instance_id = 76136
_gnb_0_global_bts_id = 76136

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.164.136/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
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
        username="root",
        password="umniedziala",
     ),
     radio_type="AWEUC",
     serial_number="AH211100110",
     product_code="475168A.103",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.103",
    serial_number="DH224013224",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_0_radio_unit_0],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------GNB1_CONFIGURATION------------------------

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK136-2.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_1_instance_id = 76138
_gnb_1_global_bts_id = 76138

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=1,
)

_gnb_1_xnc_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_xnu_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_ngc_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_ngu_ip = NetworkAddress(
    v4="10.84.164.138/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=1,
)

_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_oam_ip,
    oam_ssh_connection_details=_gnb_1_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_1_oam_http_connection,
    f1m=_gnb_1_f1m_ip,
    f1c=_gnb_1_f1c_ip,
    f1u=_gnb_1_f1u_ip,
    x2c=_gnb_1_x2c_ip,
    x2u=_gnb_1_x2u_ip,
    s1c=_gnb_1_s1c_ip,
    s1u=_gnb_1_s1u_ip,
    xnc=_gnb_1_xnc_ip,
    xnu=_gnb_1_xnu_ip,
    ngc=_gnb_1_ngc_ip,
    ngu=_gnb_1_ngu_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1_radio_unit_0 = RU(
     ru_hw_group="AWGUC",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AWGUC",
     serial_number="AH234500011",
     product_code="475946A.103",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_1_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_1_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.103",
    serial_number="DH224715662",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_1_radio_unit_0],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_1_airscale = Airscale(
    core_units=[_gnb_1_core_unit_0],
    product_code="N/A",
    )

_du_gnb_1 = DU(
    airscale=_gnb_1_airscale,
    oam_ip=_gnb_1_oam_ip,
    f1_m_ip_addr=_gnb_1_f1m_ip,
    f1_c_ip_addr=_gnb_1_f1c_ip,
    f1_u_ip_addr=_gnb_1_f1u_ip,
    f1_m_cu=_gnb_1_f1m_ip,
    f1_c_cu=_gnb_1_f1c_ip,
    f1_u_cu=_gnb_1_f1u_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
    )

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_MULTIGNB_SA_QC_ASOE_AWEUC"
)

__all__ = ["tl"]
