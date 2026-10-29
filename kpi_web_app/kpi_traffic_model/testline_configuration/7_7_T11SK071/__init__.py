# Generated with TL configuration generator at 2025-02-20_08:04:06

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
from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAndroid,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml

from taf.config.testline.attenuator import RadioRack, JFW
from taf.config.testline.dcap import DcapBasic

# ------------------------UTF_CONFIGURATION------------------------

_utf = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="p04-utf-015.p04.ska-lab.nsn-rdnet.net",
        username="utfuser",
        password="utfadmin!",
        port=443,
    ),
)
# ------------------------PDU_CONFIGURATION------------------------

_dc_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="FPFH-ZK02-21-P11.p11-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    # "userName": "administrator",
    # "authKey": "password",
    # "privKey": "password",
    "userName": "user-lab0",
    "authKey": "NokiaBts2003",
    "privKey": "NokiaBts2003",
    "authProtocol": "MD5",
    "privProtocol": "AES",  # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_ac_pdu_1 = HPE(
    port_numbers=[18, 23, 24],
    addr="ZK02.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_attenuator1 = JFW(
    ip_addr="10.255.41.44",
    port=3001,
    attenuation_port_numbers=range(1, 13),
    serial_number="684067",
    model="50PA-628",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK071-1.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 81071
_gnb_0_global_bts_id = 81071

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.28.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.48.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.48.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.28.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.255.48.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.28.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.82.30.71/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
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
    ru_hw_group="AHIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHIB",
    serial_number="EA173313196",
    product_code="474050A.102",
    pdu_port=_dc_pdu_1.pdu_ports[5],
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHFB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHFB",
    serial_number="AH211300313",
    product_code="474036A.103",
    pdu_port=_dc_pdu_1.pdu_ports[6],
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104670",
    product_code="475266A.101",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.102",
    serial_number="L1214908871",
    mac_addr="00:77:e4:a6:2c:8",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=_dc_pdu_1.pdu_ports[1],
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
    dcap=_utf,
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
        addr="7-7-T11SK071-2.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_1_instance_id = 81077
_gnb_1_global_bts_id = 81077

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.82.28.77/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.82.28.77/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.28.77/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="10.255.48.77/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="10.255.48.77/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
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
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AWEUA",
    serial_number="AH204600565",
    product_code="475166A.103",
    pdu_port=_ac_pdu_1.pdu_ports[23],
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_1_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232807069",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_1_radio_unit_0],
)

_gnb_1_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_1_primary_ssh_lmp_connection,
    capacity_units=[_gnb_1_capacity_unit_0],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406209",
    mac_addr="28:74:f5:0b:58:83",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=_dc_pdu_1.pdu_ports[2],
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_common_unit_0],
    product_code="473098A",
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
    dcap=_utf,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------GNB2_CONFIGURATION------------------------

_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK071-3.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_2_instance_id = 81062
_gnb_2_global_bts_id = 81062

_gnb_2_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_2.default_ssh_connection_details,
)

_gnb_2_oam_ip = NetworkAddress(
    v4="10.82.28.62/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_2_f1m_ip = NetworkAddress(
    v4="10.82.28.62/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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
    v4="10.82.28.62/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_2_x2u_ip = NetworkAddress(
    v4="10.255.48.62/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_2_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_s1u_ip = NetworkAddress(
    v4="10.255.48.62/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_2_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_2_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
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
    ru_hw_group="AHGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHGB",
    serial_number="EB213060145",
    product_code="474514A.102",
    pdu_port=_dc_pdu_1.pdu_ports[4],
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_2_radio_unit_1 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AWEUA",
    serial_number="AH224002454",
    product_code="475166A.104",
    pdu_port=_ac_pdu_1.pdu_ports[24],
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_2_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1220903721",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_2_radio_unit_1],
)

_gnb_2_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH214748338",
    product_code="475266A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_2_radio_unit_0],
)

_gnb_2_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_2_primary_ssh_lmp_connection,
    capacity_units=[_gnb_2_capacity_unit_0, _gnb_2_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1192114420",
    mac_addr="78:f9:b4:a3:5d:20",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=_dc_pdu_1.pdu_ports[3],
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
    dcap=_utf,
)

_test_pc_gnb_2.connections = [
    Connection(
        device=_gnb_2.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_appsrv = TafUeAppServer(
    app_server_name="SKA-HC14-15",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
    expected_prompt="\~\\$",
)

_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appsrv,
    binary_path="/data/data/com.nokia.android.application/",
)

_uepc_addr = "PLKR-ZK2-BF-PC3.p11.ska-lab.nsn-rdnet.net"
_uepc_user = "plkrsg4"
_uepc_pass = "Rz0dkiewk@2024"
_ue_1_adb_sn = "R3CWC0A2ACB"
_uepc_ssh = SshServiceDetails(addr=_uepc_addr, username=_uepc_user, password=_uepc_pass)

_ue_1_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    ue_pc_port="80",
    serial_number=_ue_1_adb_sn,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1, _gnb_2],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1, _test_pc_gnb_2],
    ues=[_ue_1_android],
    attenuators=[_attenuator1],
    pdus=[_dc_pdu_1, _ac_pdu_1],
    tl_cloud_topology="CLOUD_7_7_T11SK071",
)

__all__ = ["tl"]
