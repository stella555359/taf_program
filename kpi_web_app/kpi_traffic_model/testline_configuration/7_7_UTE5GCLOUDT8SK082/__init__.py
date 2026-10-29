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
from taf.config.testline.lmi import SerialOverTcp, Remote, LMI, SerialOverHost, Local
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------
_fpfh1_pdu = FPFH(
    port_numbers=[3],
    addr="fpfh-zm03-29-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh2_pdu = FPFH(
    port_numbers=[4, 5],
    addr="fpfh-zm03-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)


_fpfh3_pdu = FPFH(
    port_numbers=[4, 5, 6],
    addr="fpfh-zm03-11-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK082.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_mumin_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="PLKR-TP-UE95.p08.ska-lab.nsn-rdnet.net",
        username="plkrsg09",
        password="ssp123!!Macro",
    )
)

_gnb_0_instance_id = 79082
_gnb_0_global_bts_id = 79082

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.152.82/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.82/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="10.84.152.82/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.152.82/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.152.82/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="/0", routing_v4=RoutingInformation(gateway="", destIpAddr=""), vlan_id=0
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
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH200900053",
    product_code="474609A.103",
    pdu_port=_fpfh3_pdu.pdu_ports[5],
    lmi=SerialOverHost(host=_mumin_pc, uart_mapping=[Local(port="COM31")]),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH195105125",
    product_code="474609A.103",
    pdu_port=_fpfh3_pdu.pdu_ports[6],
    lmi=SerialOverHost(host=_mumin_pc, uart_mapping=[Local(port="COM30")]),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH201501319",
    product_code="474609A.103",
    pdu_port=_fpfh3_pdu.pdu_ports[4],
    lmi=SerialOverHost(host=_mumin_pc, uart_mapping=[Local(port="COM29")]),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203902604",
    product_code="474020B.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="EA193273724",
    product_code="474020A.102",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_1],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1184409447",
    product_code="474020A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_2],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIK",
    hardware_version="A.102",
    serial_number="EA200261173",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=_fpfh2_pdu.pdu_ports[5],
)

_gnb_0_airscale = Airscale(common_units=[_gnb_0_common_unit_0], product_code="473098A")

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
    tl_cloud_topology="CLOUD_7_7_T8SK082",
    pdus=[_fpfh1_pdu, _fpfh2_pdu, _fpfh3_pdu],
)

__all__ = ["tl"]
