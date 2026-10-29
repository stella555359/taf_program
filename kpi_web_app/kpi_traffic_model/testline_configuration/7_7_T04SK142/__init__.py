# Generated with TL configuration generator at 2024-07-09_10:13:09

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Patryk Wojcik"
__team__ = "MN_RAN_RD_VRF_KRK_3"
__email__ = "patryk.wojcik@nokia.com"

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

# ---------------------UTE_UE Env-----------------------------------
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
    port_numbers=[4],         # update port_no
    addr="fpfh-za07-48-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "user-lab0",
    "authKey": "NokiaBts2003",
    "privKey": "NokiaBts2003",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[2,3],         # update port_no
    addr="za07.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T04SK142.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 77142
_gnb_0_global_bts_id = 77142

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.190.142/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.190.142/23",
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
    v4="10.84.148.142/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.20.142/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.22.142/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
     serial_number="AH204000852",
     product_code="475001A.101",
)

_gnb_0_radio_unit_0 = RU(
     ru_hw_group="AEWB",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ="),
     radio_type="AWEUA",
     serial_number="AH220600191",
     product_code="474609A.105",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
     ru_hw_group="AWEUA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="tC0p5lpI9l/jX3RLphVLv+nxJ4P32DnqZlLyU9wkmeQ="),
     radio_type="AWEUA",
     serial_number="AH204500786",
     ru_extensions=[_gnb_0_ru_extension_unit_0],
     product_code="475166A.103",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIP",
    hardware_version="A.101",
    serial_number="L1231800072",
    product_code="475792A.101",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_0],
    )

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232804661",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_1],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233304604",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),    # uncomment & update port_no for gNB - for eNB you can delete
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
    tl_cloud_topology="CLOUD_7_7_T04SK142"
)

cred1 = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="BTSSecurity",
    password="Nemu@123",
    port=443,
)

cred2 = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="BTSApplication",
    password="Nemu@123",
    port=443,
)

cred3 = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="BTSRead",
    password="Nemu@123",
    port=443,
)

creds=[_gnb_0_oam_http_connection,cred1, cred2, cred3]

tl.creds = creds

__all__ = ["tl"]
