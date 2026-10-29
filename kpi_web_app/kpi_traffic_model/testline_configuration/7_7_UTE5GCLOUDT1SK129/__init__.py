__maintainer__ = "Wioleta Swies"
__team__ = "MN RAN Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"
__owner_email__ = "wioleta.swies@gmail.com"


from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu, FPFH
import os
import yaml

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.164.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.164.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
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
    v4="10.255.6.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=505,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.8.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=506,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.8.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.255.6.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=505,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.8.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=506,
)

_gnb_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.8.129/23",
    routing_v4=RoutingInformation(gateway="10.255.9.254", destIpAddr="10.83.160.0"),
    vlan_id=506,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK129.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 76129
_gnb_global_bts_id = 76129

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

# ------------------------PDU_CONFIGURATION------------------------

_pdu_ru = FPFH(
    addr="fpfh-ze18-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_ru_pdu_port = PduPort(pdu=_pdu_ru, port_no=6)

_pdu_smod = FPFH(
    addr="fpfh-ze18-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_common_unit_pdu_port = PduPort(pdu=_pdu_smod, port_no=3)

# ------------------------------------------------------------------

gnb_radio_unit_0 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="umniedziala"
    ),
    radio_type="AHFIG",
    serial_number="BL2233W2CRM",
    product_code="475125A.101",
    pdu_port=_ru_pdu_port,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1214902976",
    product_code="475266A.103",
    # slot_id=SlotId.B1
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.102",
    serial_number="L1220500508",
    mac_addr="",
    pdu_port=_common_unit_pdu_port,
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

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

# ------------------------TL_CONFIGURATION------------------------

_test_pc_gnb.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_ABIO_AHIG_ENB_ANDROID",
)

__all__ = ["tl"]
