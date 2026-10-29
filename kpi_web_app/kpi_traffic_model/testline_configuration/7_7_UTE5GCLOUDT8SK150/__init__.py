__maintainer__ = "Monika Mysliwiec"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "monika.mysliwiec@nokia.com"

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
from taf.config.testline.enb import RealEnb
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zh14-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
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
    port_numbers=[999],
    addr="zh14.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.84.152.150/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK150.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 79150
_gnb_global_bts_id = 79150

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
        addr="", username="root", password="umniedziala"
    ),
    radio_type="APHG",
    serial_number="NH210200277",
    product_code="475295A.101S",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=6),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="APHG",
    serial_number="NH213100554",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=10),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="APHG",
    serial_number="NH230600474",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=9),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="ute@7-7-UTE5GCLOUDT8SK150:~$",
    hardware_type="ABIP",
    hardware_version="A.101",
    serial_number="L1231800033",
    product_code="475792A.101",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIM",
    hardware_version="A.103",
    serial_number="L1231204146",
    mac_addr="",
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
)

_airscale_gnb = Airscale(common_units=[_gnb_common_unit_0], product_code="473098A")

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

# ------------------------TL_CONFIGURATION------------------------
tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASIMR_ABIPB4_3xAPHG_6xAWHGEQH",
)

__all__ = ["tl"]
