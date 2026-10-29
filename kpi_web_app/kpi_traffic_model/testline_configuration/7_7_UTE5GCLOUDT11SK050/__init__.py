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
    port_numbers=[3],
    addr="fpfh-zm04-47-p11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(
    port_numbers=[4, 5, 6],
    addr="fpfh-zm04-35-p11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.82.28.50/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.82.28.50/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.30.50/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.48.50/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.50.50/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
        addr="7-7-UTE5GCLOUDT11SK050.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 81050
_gnb_global_bts_id = 81050

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
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH211900319",
    product_code="474609A.105",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=4),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH194806877",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=5),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH201501310",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=6),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1212903707",
    product_code="474020B.102",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_0],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1213310143",
    product_code="474020B.102",
    slot_id=SlotId.B3,
    rus=[_gnb_radio_unit_2],
)

_gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1212704290",
    product_code="474020B.102",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_1],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1, _gnb_capacity_unit_2],
    hardware_type="ASIK",
    hardware_version="A.103",
    serial_number="L1204210555",
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=3),
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
    v4="10.84.152.162/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.152.162/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK162.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 79162
_enb_global_bts_id = 79162

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_radio_unit_0 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS192809059",
    product_code="473966A.101",
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="DH192352430",
    product_code="473096A.103",
    slot_id=SlotId.B1,
    rus=[_enb_radio_unit_0],
)

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="DH203360007",
    slot_id=SlotId.C1,
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
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKL_ABILB1B2B3_3xAEWB_T11SK050",
)

__all__ = ["tl"]
