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
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu, FPFH, HPE

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.140.99/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
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
    v4="10.84.142.99/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.140.99/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.140.99/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
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

# gNB test VM

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK099.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 80099
_gnb_global_bts_id = 80099

# Power breakers

_gnb_pdu = FPFH(
    addr="fpfh-zc16-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1],
)

_default_ssh_lmp_connection = SshServiceDetails(
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

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_pdu_gnb_ru = HPE(
    addr="zc16.mgt.ska-lab.nsn-rdnet.net", port_numbers=[2], snmp_user=_snmp_user
)

# 5G Radio units

gnb_radio_unit_0 = RU(
    ru_hw_group="ASiR-HUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHA",
    serial_number="NH224300867",
    pdu_port=_pdu_gnb_ru.pdu_ports[2],
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
    addr="0.0.0.0",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223610404",
    product_code="475266A.104",
    # slot_id=SlotId.B1,    # ?
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1204906621",
    mac_addr="",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=1),  # ?
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")


_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0],
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
# ------------------------TL_CONFIGURATION------------------------
_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_APHA_2xAWHHC_2xAHENB",
)

__all__ = ["tl"]
