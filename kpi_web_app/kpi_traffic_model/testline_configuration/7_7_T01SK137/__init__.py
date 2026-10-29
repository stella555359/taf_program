# Generated with TL configuration generator at 2024-09-26_11:45:19

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
from taf.config.testline import TafUeAppServer, TafUeDataTransferProtocol, TafUeAndroid
from taf.config.testline.lmi import SerialOverTcp, Remote
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1],
    addr="fpfh-zc09-38-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "user-lab0",
    "authKey": "NokiaBts2003",
    "privKey": "NokiaBts2003",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_pdu = HPE(
    port_numbers=[4],
    addr="zc16.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01SK137.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 76137
_gnb_0_global_bts_id = 76137

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.164.137/23",
    routing_v4=RoutingInformation(gateway="10.255.7.254", destIpAddr="10.83.249.104"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.164.137/23",
    routing_v4=RoutingInformation(gateway="10.255.7.254", destIpAddr="10.83.249.104"),
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
    v4="10.84.150.137/23",
    routing_v4=RoutingInformation(gateway="10.255.7.254", destIpAddr="10.83.249.104"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.6.137/23",
    routing_v4=RoutingInformation(gateway="10.255.7.254", destIpAddr="10.83.249.104"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.8.137/23",
    routing_v4=RoutingInformation(gateway="10.255.7.254", destIpAddr="10.83.249.104"),
    vlan_id=506,
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
     ru_hw_group="AWKUC",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
     ),
     radio_type="AWKUC",
     serial_number="AH241600647",
     product_code="476239A.101",
     # pdu_port=PduPort(pdu=_ru_pdu, port_no=4),
     pdu_port=_ru_pdu.pdu_ports[4],
     lmi=SerialOverTcp(
         uart_mapping=[Remote(addr=NetworkAddress(v4="mumin-zc10-06-p01.p01-leg.ska-lab.nsn-rdnet.net"), port=5001)]
     )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A.101",
    serial_number="L1231505879",
    product_code="475792A.101",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1234607614",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="474767A",
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
        addr="7-7-UTE5GCLOUDT9SK009.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_0_instance_id = 80009
_enb_0_global_bts_id = 80009

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.140.9/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.9/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_radio_unit_0 = RU(
     ru_hw_group="AHEGA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AHEGA",
     serial_number="EA222450171",
     product_code="473995A.101",
     # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="EA195163101",
    product_code="473096A.104",
    slot_id=SlotId.B4,
    rus=[_enb_0_radio_unit_0],
    )

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="EA195254953",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------TafUeAndroid--------------------

# _appsrv = TafUeAppServer(
#     app_server_name="SKA-HC14-15",
#     address="10.84.168.120",
#     bind_interface_ip="10.84.169.60",
#     user="5g",
#     password="5g"
# )

# _appsrv = TafUeAppServer(
#     app_server_name="SKA-HC14s17-1",
#     address="10.84.168.70",
#     bind_interface_ip="10.84.169.54",
#     user="5g",
#     password="5g"
# )
#
# _appsrv = TafUeAppServer(
#     app_server_name="SKA-HC14s17-3",
#     address="10.84.168.72",
#     bind_interface_ip="10.84.169.56",
#     user="5g",
#     password="5g1$NEWradio"
# )

_appsrv = TafUeAppServer(
    app_server_name="SKA-HC14s18-2",
    address="10.84.168.79",
    bind_interface_ip="10.84.169.51",
    user="5g",
    password="5g"
)

_iperf = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_appsrv,
    binary_path='/data/data/com.nokia.android.application/',
    interval=1,
)

_sdx_75 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="plkr-zc09-pc2.p01.ska-lab.nsn-rdnet.net",
        username="plkrsg4",
        password="Rz0dkiewk@2024",
    ),
    ue_pc_address="plkr-zc09-pc2.p01.ska-lab.nsn-rdnet.net",
    ue_pc_port="8080",
    serial_number="e3123725",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    ues=[_sdx_75],
    pdus=[_bts_pdu, _ru_pdu],
    tl_cloud_topology="CLOUD_7_7_T01SK137"
)

__all__ = ["tl"]
