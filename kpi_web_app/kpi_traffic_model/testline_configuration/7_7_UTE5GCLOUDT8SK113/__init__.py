__maintainer__ = "Mateusz Iwankiewicz"
__team__ = "I_MN_RAN_PZ_KRK_SG_8_GMS"
__email__ = "I_MN_RAN_PZ_KRK_SG_8@internal.nsn.com"
__owner_email__ = "mateusz.iwankiewicz@nokia.com"

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
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg06-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg06-31-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg05-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_3 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zh06-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_4 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg04-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.113/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.113/23",
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
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
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

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK113-1.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 79113
_gnb_global_bts_id = 79113

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

_secondary_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.119",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_gnb_radio_unit_0 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1930G11NT",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=3),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIG",
    serial_number="BL2245W2M0M",
    product_code="475125A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=2),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1930G11NK",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_4, port_no=3),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIG",
    serial_number="BL2233W2DDD",
    product_code="475125A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),
)

_gnb_radio_unit_4 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1933G10RE",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=4),
)

_gnb_radio_unit_5 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIG",
    serial_number="BL2220W2U01",
    product_code="475125A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=3),
)

_gnb_radio_unit_6 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIG",
    serial_number="BL2220W2U00",
    product_code="475125A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=4),
)

_gnb_radio_unit_7 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1932G1YIT",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=5),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-0a:~",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1174808895",
    product_code="473096A.103",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_2, _gnb_radio_unit_4, _gnb_radio_unit_7],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1171720871",
    product_code="473096A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_5],
)

_gnb_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="K9173842014",
    product_code="473096A.103",
    slot_id=SlotId.B3,
    rus=[_gnb_radio_unit_6],
)

_gnb_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="EA183942878",
    product_code="473096A.103",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_1, _gnb_radio_unit_3],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_secondary_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="AH191100403",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=5),
)

_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_1, _gnb_capacity_unit_2, _gnb_capacity_unit_3],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="AH184701833",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=6),
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0, _gnb_common_unit_1],
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

_test_pc_gnb_smod2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK113-2.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_smod2.connections = [
    Connection(
        device=_gnb.dus[0].airscale.common_units[1],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb, _test_pc_gnb_smod2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_ASIA_ABIAB1B2B3_AHFIG-ASIA_ABIAB4_AHLOA_ENB",
)

__all__ = ["tl"]
