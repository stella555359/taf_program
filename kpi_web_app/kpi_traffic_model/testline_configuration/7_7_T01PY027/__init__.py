# Generated with TL configuration generator at 2026-03-17_15:20:25

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
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[4, 5],         # update port_no
    addr="http://fpfh-pd21-19-d01.d01-leg.krk-lab.nsn-rdnet.net/",   # update address
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(
    port_numbers=[6],         # update port_no
    addr="http://fpfh-pc08-46-d01.d01-leg.krk-lab.nsn-rdnet.net/",    # update address
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY027-1.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 85027
_gnb_0_global_bts_id = 85027

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
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
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.89.4.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.254.4.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.89.4.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.254.4.27/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
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
    ru_hw_group="AREA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AREA",
    serial_number="K9221528889",
    product_code="474198A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=6
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613129",
    product_code="475266A.105",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613325",
    product_code="475266A.105",
    slot_id=SlotId.B3,
    rus=[],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613130",
    product_code="475266A.105",
    slot_id=SlotId.B2,
    rus=[],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH202661744",
    mac_addr="48:ec:5b:23:99:fe",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="475773A.101",
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

# ------------------------GNB1_CONFIGURATION------------------------

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY027-2.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_1_instance_id = 85028
_gnb_1_global_bts_id = 85028

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.89.3.28/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.89.3.28/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
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

_gnb_1_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1250406979",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_1_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1164712622",
    product_code="473096A.103",
    slot_id=SlotId.B5,
    rus=[],
)

_gnb_1_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613330",
    product_code="475266A.105",
    slot_id=SlotId.B6,
    rus=[],
)

_gnb_1_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_1_capacity_unit_0, _gnb_1_capacity_unit_1, _gnb_1_capacity_unit_2],
    hardware_type="ASIL",
    hardware_version="A.102",
    serial_number="L1213507375",
    mac_addr="00:77:e4:94:98:c3",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=5
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_common_unit_0],
    product_code="475773A.101",
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
        device=_gnb_1.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1],
    pdus=[_bts_pdu, _ru_pdu],
    tl_cloud_topology="CLOUD_7_7_T01PY027",

)

__all__ = ["tl"]
