# Generated with TL configuration generator at 2024-12-20_14:31:55

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
    port_numbers=[4, 6],         # update port_no
    addr="10.253.176.79",   # update address
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
    port_numbers=[12],
    addr="10.89.63.21",
    snmp_user=_hpe_snmp_user,
)

_ru_pdu_2 = HPE(
    port_numbers=[12],
    addr="gh15.mgt.krk-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT189.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 75189
_gnb_0_global_bts_id = 75189

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.182.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.182.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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
    v4="10.253.212.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.253.212.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.214.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.253.212.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.253.212.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.83.252.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.83.252.189/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
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
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH210200290",
    product_code="475295A.101S",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=19),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH211600071",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=20),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH213100514",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=12),
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA213353970",
    mac_addr="78:f9:b4:dc:79:fd",
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=6),
)

_gnb_0_airscale = Airscale(
    core_units=[_gnb_0_core_unit_0],
    product_code="N/A",
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
        device=_gnb_0.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------GNB1_CONFIGURATION------------------------

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT155.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_1_instance_id = 75155
_gnb_1_global_bts_id = 75155

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.83.182.155/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.83.182.155/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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

_gnb_1_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH211600071",
    product_code="475295A.101",
)

_gnb_1_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH213100514",
    product_code="475295A.101",
)

_gnb_1_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH210200290",
    product_code="475295A.101S",
)

_gnb_1_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_1_primary_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA213153884",
    mac_addr="78:f9:b4:da:ee:32",
    rus=[_gnb_1_radio_unit_0, _gnb_1_radio_unit_1, _gnb_1_radio_unit_2],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_1_airscale = Airscale(
    core_units=[_gnb_1_core_unit_0],
    product_code="N/A",
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
        device=_gnb_1.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------GNB2_CONFIGURATION------------------------

_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT266.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_2_instance_id = 75266
_gnb_2_global_bts_id = 75266

_gnb_2_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_2.default_ssh_connection_details,
)

_gnb_2_oam_ip = NetworkAddress(
    v4="10.83.183.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_2_f1m_ip = NetworkAddress(
    v4="10.83.183.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_2_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_x2c_ip = NetworkAddress(
    v4="10.253.213.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_2_x2u_ip = NetworkAddress(
    v4="10.253.213.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_2_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_s1u_ip = NetworkAddress(
    v4="10.253.215.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_2_xnc_ip = NetworkAddress(
    v4="10.83.253.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_2_xnu_ip = NetworkAddress(
    v4="10.253.213.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=542,
)

_gnb_2_ngc_ip = NetworkAddress(
    v4="10.83.253.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_2_ngu_ip = NetworkAddress(
    v4="10.253.215.16/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_2_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_2_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_2 = CU(
    backhaul_site_oam_ip=_gnb_2_oam_ip,
    oam_ssh_connection_details=_gnb_2_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_2_oam_http_connection,
    f1m=_gnb_2_f1m_ip,
    f1c=_gnb_2_f1c_ip,
    f1u=_gnb_2_f1u_ip,
    x2c=_gnb_2_x2c_ip,
    x2u=_gnb_2_x2u_ip,
    s1c=_gnb_2_s1c_ip,
    s1u=_gnb_2_s1u_ip,
    xnc=_gnb_2_xnc_ip,
    xnu=_gnb_2_xnu_ip,
    ngc=_gnb_2_ngc_ip,
    ngu=_gnb_2_ngu_ip,
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
)

_gnb_2_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHA",
    serial_number="NH224900144",
    product_code="474657A.103",
)

_gnb_2_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="toor4nsn",
       password="oZPS0POrRieRtu",
    ),
    radio_type="APHG",
    serial_number="NH213100504",
    product_code="475295A.101",
)

_gnb_2_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1215008546",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[],
    )

_gnb_2_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.103",
    serial_number="L1214007309",
    product_code="474824A.103",
    slot_id=SlotId.B1,
    rus=[],
    )

_gnb_2_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_2_primary_ssh_lmp_connection,
    capacity_units=[_gnb_2_capacity_unit_0, _gnb_2_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH220146592",
    mac_addr="60:8f:a4:50:d7:22",
    slot_id=SlotId.C1,
)

_gnb_2_airscale = Airscale(
    common_units=[_gnb_2_common_unit_0],
    product_code="473098A",
    )

_du_gnb_2 = DU(
    airscale=_gnb_2_airscale,
    oam_ip=_gnb_2_oam_ip,
    f1_m_ip_addr=_gnb_2_f1m_ip,
    f1_c_ip_addr=_gnb_2_f1c_ip,
    f1_u_ip_addr=_gnb_2_f1u_ip,
    f1_m_cu=_gnb_2_f1m_ip,
    f1_c_cu=_gnb_2_f1c_ip,
    f1_u_cu=_gnb_2_f1u_ip,
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
    )

_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id=_gnb_2_instance_id,
    global_bts_id=_gnb_2_global_bts_id,
)

_test_pc_gnb_2.connections = [
    Connection(
        device=_gnb_2.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1, _gnb_2],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology="Please complete the cloud topology or remove this line"
)

__all__ = ["tl"]
