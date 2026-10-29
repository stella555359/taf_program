# Generated with TL configuration generator at 2024-08-28_08:43:38

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[3, 4],         # update port_no
    addr="fpfh-hi07-46-p11.p11-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[9, 10, 11],         # update port_no
    addr="hi07.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK018.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 81018
_gnb_0_global_bts_id = 81018

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.18/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.18/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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
    v4="10.82.28.18/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.82.28.18/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.82.28.18/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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

_gnb_0_radio_unit_0 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHA",
     serial_number="NH203500458",
     product_code="474657A.102",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=9),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHA",
     serial_number="NH193300334",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=10),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="root",
        password="umniedziala",
     ),
     radio_type="APHG",
     serial_number="NH210200283",
     product_code="475295A.101S",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=11),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH220745563",
    product_code="475266A.103",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_2],
    )

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1221404618",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
    )

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1201005372",
    product_code="474020A.102",
    slot_id=SlotId.B3,
    rus=[],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1203606132",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=3),
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

# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK019.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_enb_0_instance_id = 81019
_enb_0_global_bts_id = 81019

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.82.28.19/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.19/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203791442",
    product_code="473096A.105",
    slot_id=SlotId.B4,
    rus=[],
    )

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="EA194850497",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="473098A",
    )

_enb_0 = RealEnb(
    x2_link_addr=_enb_0_oam_ip,
    instance_id=_enb_0_instance_id,
    global_bts_id=_enb_0_global_bts_id,
    system_module=_enb_0_airscale,
    oam_ip=_enb_0_oam_ip,
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    tl_cloud_topology="Please complete the cloud topology or remove this line"
)

__all__ = ["tl"]