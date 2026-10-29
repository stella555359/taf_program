__maintainer__ = "Piotr Brzezicki"
__team__ = "MN RAN RD VRF KRK 6"
__email__ = "piotr.brzezicki@nokia.com"

from taf.config.testline import TafUeDataTransferProtocol, TafUeAppServer, TafUeAndroid
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

# ------------------------PDU_CONFIGURATION------------------------

_fpfh_zg13_46 = FPFH(
    port_numbers=[5, 6],
    addr="fpfh-zg13-46-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh_zh14_48 = FPFH(
    port_numbers=[2],
    addr="fpfh-zh14-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh_zh16_46 = FPFH(
    port_numbers=[4],
    addr="fpfh-zh16-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh_zh15_46 = FPFH(
    port_numbers=[6],
    addr="fpfh-zh15-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_fpfh_zg14_26 = FPFH(
    port_numbers=[6],
    addr="fpfh-zg14-26-p08.p08-leg.ska-lab.nsn-rdnet.net",
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

_hpe_zg16 = HPE(
    port_numbers=[10, 11],
    addr="zg16.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T08SK042-1.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 79042
_gnb_0_global_bts_id = _gnb_0_instance_id

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.152.42/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.42/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.152.42/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.28.42/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.28.42/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
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
    ru_hw_group="5Ggen5_2T2R",
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
    radio_type="AWEUA",
    serial_number="AH243801875",
    product_code="475166A.105",
    pdu_port=PduPort(pdu=_hpe_zg16, port_no=11),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="5Ggen5_2T2R",
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
    radio_type="AWEWA",
    serial_number="YK212500121",
    product_code="475170A.101",
    pdu_port=PduPort(pdu=_hpe_zg16, port_no=10),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="mmWRF7.1_8T8R",
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
    radio_type="AWKUD",
    serial_number="AH243705768",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_fpfh_zg14_26, port_no=6),
)

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOH",
    hardware_version="A.102",
    serial_number="L1243307843",
    mac_addr="d0:48:4f:07:0c:32",
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
    pdu_port=PduPort(pdu=_fpfh_zg13_46, port_no=5),
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

# ------------------------ENB0_CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T08SK042-2.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_0_instance_id = 79086
_enb_0_global_bts_id = _enb_0_instance_id

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.84.152.86/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.86/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_radio_unit_0 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHEGC",
    serial_number="EA205053928",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_fpfh_zh16_46, port_no=4),
)

_enb_0_radio_unit_1 = RU(
    ru_hw_group="AHIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="",
        password="",
    ),
    radio_type="AHEGC",
    serial_number="EA174610766",
    product_code="474050A.102",
    pdu_port=PduPort(pdu=_fpfh_zh15_46, port_no=6),
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.106",
    serial_number="DH204991663",
    product_code="473096A.106",
    slot_id=SlotId.B1,
    rus=[_enb_0_radio_unit_0, _enb_0_radio_unit_1],
)

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[_enb_0_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="L1172815408",
    mac_addr="d8:ef:cd:29:b9:72",
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_fpfh_zh14_48, port_no=2),
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

_test_pc_enb_0.connections = [
    Connection(
        device=_enb_0.system_module.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_appsrv_vm1 = TafUeAppServer(
    app_server_name="SKA-HC14-15",
    address="SKA-HC14-15-AppServer.p00-hc14.ska-lab.nsn-rdnet.net",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
    expected_prompt="\~\$",
)

_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appsrv_vm1,
    binary_path="/data/data/com.nokia.android.application/",
)

_uepc_addr = "PLKR-SG06-15.INTRA.NOKLAB.NET"
_uepc_user = "pzkrk"
_uepc_pass = "NokiaBts2003"
_uepc_ssh = SshServiceDetails(addr=_uepc_addr, username=_uepc_user, password=_uepc_pass)

_ue_1_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    proxy_mngr_port="9955",
    serial_number="e5e1d9d4",
    capabilities=["MTP_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

_ue_2_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    proxy_mngr_port="9955",
    serial_number="RFCWC0YTNBY",
    capabilities=["COMMERCIAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

_ue_3_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    proxy_mngr_port="9955",
    serial_number="RFCX205N8RR",
    capabilities=["COMMERCIAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_enb_0],
    ues=[_ue_1_android, _ue_2_android, _ue_3_android],
    tl_cloud_topology="CLOUD_7_7_T08SK042",
)

__all__ = ["tl"]
