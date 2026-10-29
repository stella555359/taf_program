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

_bts_pdu = FPFH(
    port_numbers=[2],         # update port_no
    addr="fpfh-za01-48-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
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
    port_numbers=[9, 10, 11, 12, 13, 14],         # update port_no
    addr="za01.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
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
    v4="10.84.190.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.20.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.148.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.20.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=505,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.190.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=504,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.20.79/23",
    routing_v4=RoutingInformation(gateway="10.255.21.254", destIpAddr="10.89.169.0"),
    vlan_id=505,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK079.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77079
_gnb_global_bts_id = 77079

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
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.6",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600432",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=10),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.10",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600442",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=11),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_2 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.158",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600437",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=13),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_3 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.162",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600440",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=14),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_4 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.154",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600482",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=12),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_5 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH230600434",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=9),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH222840138",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2, _gnb_radio_unit_3, _gnb_radio_unit_4, _gnb_radio_unit_5],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1224211812",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------UE_CONFIG-------------------------------

def _set_abstract_lib_config_env(ue_config_file):  # <----------
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config

ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
	tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASILR_ABIOB4_6xAPHG_7xAWHHC",
)
tl.ue_config = ue_config
__all__ = ["tl"]


