# Generated with TL configuration generator at 2023-12-19_14:55:47

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
from taf.config.testline.radio import RU
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline import TafUeAppServer, TafUeDataTransferProtocol, TafUeAndroid
from taf.config.testline.radio import Positioner1DKrk

# ------------------------PDU_CONFIGURATION------------------------

_bts_0_pdu = FPFH(
    port_numbers=[1],
    addr="fpfh-ze07-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
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

_ru_0_pdu = HPE(
    port_numbers=[2],
    addr="ze07.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_ue_pdu = HPE(
    port_numbers=[5],
    addr="zf07.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

_bts_1_pdu = FPFH(
    port_numbers=[3],
    addr="fpfh-ze07-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_1_pdu = FPFH(
    port_numbers=[2],
    addr="fpfh-ze07-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_enb_pdu = FPFH(
    port_numbers=[2, 4],
    addr="fpfh-zf07-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------POSITIONER_CONFIGURATION------------------------

_positioner = Positioner1DKrk(
    default_ssh_connection_details=SshServiceDetails(
        addr="tty-server199.p04.ska-lab.nsn-rdnet.net",
        username="emssim",
        password="emssim4Krakow$")
)

# ------------------------GNB0_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.50/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.50/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.190.50/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.190.50/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.190.50/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK050.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77050
_gnb_global_bts_id = 77050

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],  # Check and replace in script
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
     ru_hw_group="AWEUA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AWEUA",
     serial_number="AH205100796",
     product_code="475166A.103",
     pdu_port=PduPort(pdu=_ru_0_pdu, port_no=2),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203611861",
    product_code="474020B.102",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_0],
    )

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203611823",
    product_code="474020B.102",
    slot_id=SlotId.B1,
    rus=[],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIK",
    hardware_version="A.103",
    serial_number="L1204210571",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_0_pdu, port_no=1),
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

_gnb_0 = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------GNB1_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.44/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.44/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.148.44/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.20.44/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.44/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK044.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77044
_gnb_global_bts_id = 77044

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
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
     ru_hw_group="AEUD",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="AEUD",
     serial_number="AH200704752",
     product_code="474611A.102",
     positioner=_positioner,
     pdu_port=PduPort(pdu=_ru_1_pdu, port_no=2),
)

_gnb_core_unit_0 = CoreUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.101",
    serial_number="EA211854202",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_radio_unit_0],
    pdu_port=PduPort(pdu=_bts_1_pdu, port_no=3),
)

_airscale_gnb = Airscale(
    core_units=[_gnb_core_unit_0],
    product_code="N/A",
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

_gnb_1 = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.190.49/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.190.49/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK049.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
    # connections are not defined because we do not want to perform yaft by
    # CommonAgent (eNb is usually shared between many gNBs)
)

_enb_instance_id = 10049
_enb_global_bts_id = 10049

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
     serial_number="AS210708412",
     product_code="473966A.101",
     pdu_port=PduPort(pdu=_enb_pdu, port_no=4),
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="DH192352347",
    product_code="473096A.103",
    slot_id=SlotId.B4,
    rus=[_enb_radio_unit_0],
    )

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="DH202960708",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_enb_pdu, port_no=2),
)

_airscale_enb = Airscale(
    common_units=[_enb_common_unit_0],
    product_code="N/A",
    )

_enb = RealEnb(
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------TafUeAndroid--------------------

_appsrv = TafUeAppServer(
    app_server_name="SKA-HC14-16",
    address="10.84.168.121",
    bind_interface_ip="10.84.169.61",
    user="5g",
    password="5g"
)

_iperf = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_appsrv,
    interval=1,
)

_mtk = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-SC5G-UE286.p04.ska-lab.nsn-rdnet.net",
        username="plkrsg4",
        password="Rz0dkiewk@2024",
    ),
    ue_pc_address="PLKR-SC5G-UE286.p04.ska-lab.nsn-rdnet.net",
    ue_pc_port="8080",
    serial_number="0123456789ABCDEF",
    data_transfer=[_iperf],
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb],
    ues=[_mtk],
    pdus=[_ue_pdu, _bts_0_pdu, _ru_0_pdu, _bts_1_pdu, _ru_1_pdu],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIK_2xABIL_AWEUA",
)

__all__ = ["tl"]
