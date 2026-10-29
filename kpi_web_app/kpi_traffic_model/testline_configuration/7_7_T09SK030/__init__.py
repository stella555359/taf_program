# Generated with TL configuration generator at 2023-07-19_13:16:55

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
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FPFH, HPE
from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAndroid,
    TafUeAt,
)
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.lmi import SerialOverTcp, Remote
from taf.config.testline.dcap import DcapBasic
import ipaddress

_PROXY_MNGR_PORT = 9955
_HTTPS_PORT = 443
_UTE_USERNAME = "ute"
_UTE_PASSWORD = "ute"
_LMP_ADDR = "192.168.255.129"
_LMP_USERNAME = "toor4nsn"
_LMP_PASSWORD = "oZPS0POrRieRtu"
_NEMU_USERNAME = "Nemuadmin"
_NEMU_PASSWORD = "nemuuser"
_FPFH_PDU_USERNAME = "admin"
_FPFH_PDU_PASSWORD = "admin"
_SERVICEUSER_USERNAME = "serviceuser"
_EMPTY_ADDR = ""
_APP_SERVER_USER = "5g"
_APP_SERVER_PASSWORD = "5g"
_EXPECTED_PROMPT = r"\~\\$"

_utf = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="p04-utf-015.p04.ska-lab.nsn-rdnet.net",
        username="utfuser",
        password="utfadmin!",
        port=_HTTPS_PORT,
    ),
)

# ------------------------GNB_CONFIGURATION------------------------
_pod = "09"
_bts0_id = 30
_bts1_id = 31
_bts_id_range = 80000
_bts_0_mrbtsid = _bts_id_range + _bts0_id
_bts_0_nrbtsid = _bts_0_mrbtsid
_bts_1_mrbtsid = _bts_id_range + _bts1_id
_bts_1_nrbtsid = _bts_1_mrbtsid

_ssh_test_vm_0 = SshServiceDetails(
    addr=f"7-7-T{_pod}SK0{_bts0_id}-1.p{_pod}.ska-lab.nsn-rdnet.net",
    username=_UTE_USERNAME,
    password=_UTE_PASSWORD,
)

_ssh_test_vm_1 = SshServiceDetails(
    addr=f"7-7-T{_pod}SK0{_bts0_id}-2.p{_pod}.ska-lab.nsn-rdnet.net",
    username=_UTE_USERNAME,
    password=_UTE_PASSWORD,
)

_vlans = {
    "5g_cplane": {
        "vlan_id": 504,
        "subnet_v4": "10.84.140.0",
        "mask_v4": 23,
        "routing_v4": RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
        "subnet_v6:": "2a00:8a02:60:70::",
        "mask_v6": 64,
        "routing_v6": RoutingInformation(gateway="2a00:8a02:60:70:ffff:ffff:ffff:fffe", destIpAddr="::/0"),
    },
    "5g_uplane": {
        "vlan_id": 505,
        "subnet_v4": "10.255.34.0",
        "mask_v4": 23,
        "routing_v4": RoutingInformation(gateway="10.255.35.254", destIpAddr="0.0.0.0"),
        "subnet_v6:": "2a00:8a02:60:70::",
        "mask_v6": 64,
        "routing_v6": RoutingInformation(gateway="2a00:8a02:60:71:ffff:ffff:ffff:fffe", destIpAddr="::/0"),
    },
    "4g_uplane": {
        "vlan_id": 506,
        "subnet_v4": "10.255.36.0",
        "mask_v4": 23,
        "routing_v4": RoutingInformation(gateway="10.255.37.254", destIpAddr="0.0.0.0"),
        "subnet_v6:": "2a00:8a02:60:70::",
        "mask_v6": 64,
        "routing_v6": RoutingInformation(gateway="2a00:8a02:60:72:ffff:ffff:ffff:fffe", destIpAddr="::/0"),
    },
    "4g_cplane": {
        "vlan_id": 507,
        "subnet_v4": "10.84.142.0",
        "mask_v4": 23,
        "routing_v4": RoutingInformation(gateway="10.84.143.254", destIpAddr="0.0.0.0"),
        "subnet_v6:": "2a00:8a02:60:70::",
        "mask_v6": 64,
        "routing_v6": RoutingInformation(gateway="2a00:8a02:60:70:ffff:ffff:ffff:fffe", destIpAddr="::/0"),
    },
}

_cplane_vlan = _vlans["5g_cplane"]
_uplane_vlan = _vlans["5g_uplane"]


def _build_ip_from_vlan(vlan: dict[str, object], host_id: int) -> str:
    network = ipaddress.ip_network(f"{vlan['subnet_v4']}/{vlan['mask_v4']}", strict=False)
    return str(ipaddress.ip_address(int(network.network_address) + host_id))


_bts_0_mplane_ip = _build_ip_from_vlan(_cplane_vlan, _bts0_id)
_bts_1_mplane_ip = _build_ip_from_vlan(_cplane_vlan, _bts1_id)
_bts_0_uplane_ip = _build_ip_from_vlan(_uplane_vlan, _bts0_id)
_bts_1_uplane_ip = _build_ip_from_vlan(_uplane_vlan, _bts1_id)
_bts_0_mplane_ip_mask = f"{_bts_0_mplane_ip}/{_cplane_vlan['mask_v4']}"
_bts_1_mplane_ip_mask = f"{_bts_1_mplane_ip}/{_cplane_vlan['mask_v4']}"
_bts_0_uplane_ip_mask = f"{_bts_0_uplane_ip}/{_uplane_vlan['mask_v4']}"
_bts_1_uplane_ip_mask = f"{_bts_1_uplane_ip}/{_uplane_vlan['mask_v4']}"


_bts_0_oam_network_address = NetworkAddress(
    v4=_bts_0_mplane_ip_mask,
    routing_v4=_cplane_vlan["routing_v4"],
    vlan_id=_cplane_vlan["vlan_id"],
)

_bts_1_oam_network_address = NetworkAddress(
    v4=_bts_1_mplane_ip_mask,
    routing_v4=_cplane_vlan["routing_v4"],
    vlan_id=_cplane_vlan["vlan_id"],
)

_bts_0_ssh_lmp_connection = SshServiceDetails(
    addr=_LMP_ADDR,
    username=_LMP_USERNAME,
    password=_LMP_PASSWORD,
    proxy=_ssh_test_vm_0,
)

_bts_1_ssh_lmp_connection = SshServiceDetails(
    addr=_LMP_ADDR,
    username=_LMP_USERNAME,
    password=_LMP_PASSWORD,
    proxy=_ssh_test_vm_1,
)


_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_bts_0_oam_network_address,
    oam_ssh_connection_details=_bts_0_ssh_lmp_connection,
    oam_http_connection_details=HttpConnectionDetails(
        addr=_bts_0_mplane_ip,
        username=_NEMU_USERNAME,
        password=_NEMU_PASSWORD,
        port=_HTTPS_PORT,
    ),
    x2c=NetworkAddress(
        v4=_bts_0_mplane_ip_mask,
        routing_v4=_cplane_vlan["routing_v4"],
        vlan_id=_cplane_vlan["vlan_id"],
    ),
    x2u=NetworkAddress(
        v4=_bts_0_uplane_ip_mask,
        routing_v4=_uplane_vlan["routing_v4"],
        vlan_id=_uplane_vlan["vlan_id"],
    ),
    s1u=NetworkAddress(
        v4=_bts_0_uplane_ip_mask,
        routing_v4=_uplane_vlan["routing_v4"],
        vlan_id=_uplane_vlan["vlan_id"],
    ),
    xnc=NetworkAddress(
        v4=_bts_0_mplane_ip_mask,
        routing_v4=_cplane_vlan["routing_v4"],
        vlan_id=_cplane_vlan["vlan_id"],
    ),
    xnu=NetworkAddress(
        v4=_bts_0_uplane_ip_mask,
        routing_v4=_uplane_vlan["routing_v4"],
        vlan_id=_uplane_vlan["vlan_id"],
    ),
    ngc=NetworkAddress(
        v4=_bts_0_mplane_ip_mask,
        routing_v4=_cplane_vlan["routing_v4"],
        vlan_id=_cplane_vlan["vlan_id"],
    ),
    ngu=NetworkAddress(
        v4=_bts_0_uplane_ip_mask,
        routing_v4=_uplane_vlan["routing_v4"],
        vlan_id=_uplane_vlan["vlan_id"],
    ),
    instance_id=_bts_0_mrbtsid,
    global_bts_id=_bts_0_nrbtsid,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_bts_1_oam_network_address,
    oam_ssh_connection_details=_bts_1_ssh_lmp_connection,
    oam_http_connection_details=HttpConnectionDetails(
        addr=_bts_1_mplane_ip,
        username=_NEMU_USERNAME,
        password=_NEMU_PASSWORD,
        port=_HTTPS_PORT,
    ),
    xnc=NetworkAddress(
        v4=_bts_1_mplane_ip_mask,
        routing_v4=_cplane_vlan["routing_v4"],
        vlan_id=_cplane_vlan["vlan_id"],
    ),
    xnu=NetworkAddress(
        v4=_bts_1_uplane_ip_mask,
        routing_v4=_uplane_vlan["routing_v4"],
        vlan_id=_uplane_vlan["vlan_id"],
    ),
    instance_id=_bts_1_mrbtsid,
    global_bts_id=_bts_1_nrbtsid,
)

_fpfh_pdu_zd09_43 = FPFH(
    port_numbers=[1, 2, 3, 4],
    addr="fpfh-zd09-43-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login=_FPFH_PDU_USERNAME,
    password=_FPFH_PDU_PASSWORD,
)

_fpfh_pdu_zd08_31 = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-zd08-31-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login=_FPFH_PDU_USERNAME,
    password=_FPFH_PDU_PASSWORD,
)

_fpfh_pdu_zc12_46 = FPFH(
    port_numbers=[5],
    addr="fpfh-zc12-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login=_FPFH_PDU_USERNAME,
    password=_FPFH_PDU_PASSWORD,
)

_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_hpe_pdu_zd09 = HPE(
    port_numbers=[13],
    addr="zd09.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_snmp_user,
)

_attenuator1 = RadioRack(
    ip_addr="10.255.40.114",
    port=50000,
    attenuation_port_numbers=[
        5,
        6,
        7,
        8,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
    ],
    serial_number="RR123",
    model="32-220",
)

_ru_aheh = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    default_ssh_connection_details=SshServiceDetails(addr="", username="root", password=""),
    radio_type="AHEH",
    serial_number="EA222750816",
    product_code="474253A.101",
    pdu_port=_fpfh_pdu_zd09_43.pdu_ports[2],
    attenuation_ports=[
        _attenuator1.attenuator_ports[19],
        _attenuator1.attenuator_ports[20],
    ],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.40.111", port=2001),
        ]
    ),
)

_ru_azqo = RU(
    ru_hw_group="cMAAr6.1_8T8R_eCPRI",
    default_ssh_connection_details=SshServiceDetails(
        addr=_EMPTY_ADDR,
        username=_SERVICEUSER_USERNAME,
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZQO",
    serial_number="1M203917010",
    product_code="475288A.102",
    pdu_port=_fpfh_pdu_zd09_43.pdu_ports[3],
    attenuation_ports=[
        _attenuator1.attenuator_ports[21],
        _attenuator1.attenuator_ports[22],
        _attenuator1.attenuator_ports[23],
        _attenuator1.attenuator_ports[24],
    ],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.40.110", port=2001),
        ]
    ),
)

_test_pc_aeqp = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK010-RU1.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_aeqp_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.102.1",
    username="rfsw",
    password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    proxy=_test_pc_aeqp.default_ssh_connection_details,
)

_ru_aeqp = RU(
    ru_hw_group="cMAAr6.1_64T64R_eCPRI",
    default_ssh_connection_details=SshServiceDetails(addr=_EMPTY_ADDR,
                                                     username=_SERVICEUSER_USERNAME,
                                                     password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="),
    radio_type="AEQP",
    serial_number="1M221301195",
    product_code="475238A.102",
    pdu_port=_fpfh_pdu_zd09_43.pdu_ports[4],
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.40.113", port=2001),
        ]
    ),
    # lmi=SerialOverHost(
    #     host=TestPc(
    #         default_ssh_connection_details=SshServiceDetails(
    #             addr="PLKR-SG06-18.intra.noklab.net",
    #             username="pzkrk",
    #             password="NokiaBts2003",
    #         )
    #     ),
    #     uart_mapping=[Local(port="COM3")],
    # ),
    # lmp_connection=_aeqp_ssh_lmp_connection,
)

_ru_ahpe = RU(
    ru_hw_group="FRMr5.1_1_2T4R",
    default_ssh_connection_details=SshServiceDetails(addr=_EMPTY_ADDR, username="root", password=""),
    radio_type="AHPE",
    serial_number="1M211904018",
    product_code="475208A.101",
    pdu_port=_fpfh_pdu_zd09_43.pdu_ports[1],
    attenuation_ports=[
        _attenuator1.attenuator_ports[17],
        _attenuator1.attenuator_ports[18],
    ],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.40.112", port=2001),
        ]
    ),
)

_ru_awkud_gnb1 = RU(
    ru_hw_group="mmWRF7.1_8T8R_1D0L",
    default_ssh_connection_details=SshServiceDetails(addr=_EMPTY_ADDR,
                                                     username=_SERVICEUSER_USERNAME,
                                                     password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="),
    radio_type="AWKUD",
    serial_number="AH244201776",
    product_code="476240A.102",
    pdu_port=_fpfh_pdu_zc12_46.pdu_ports[5],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.40.86", port=2001),
        ]
    ),
)

_ru_aphg = RU(
    ru_hw_group="AUX_SC_HUB_2",
    default_ssh_connection_details=SshServiceDetails(addr="", username="toor4nsn", password="oZPS0POrRieRtu"),
    radio_type="APHG",
    serial_number="NH225300337",
    product_code="475295A.101",
    pdu_port=_hpe_pdu_zd09.pdu_ports[13],
    attenuation_ports=[
        _attenuator1.attenuator_ports[25],
        _attenuator1.attenuator_ports[26],
        _attenuator1.attenuator_ports[27],
        _attenuator1.attenuator_ports[28],
    ],
)

_gnb1_bbmod_bottom = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1250407000",
    product_code="475792A.102",
    slot_id="B1",
    rus=[_ru_awkud_gnb1],
)

_gnb0_bbmod_bottom = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1225111798",
    product_code="475266A.104",
    slot_id="B4",
    rus=[],
)

_gnb0_bbmod_top = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1215008496",
    product_code="475266A.104",
    slot_id="B6",
    rus=[_ru_azqo, _ru_aphg],
)

_gnb0_bbmod_middle = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1215008512",
    product_code="475266A.104",
    slot_id="B5",
    rus=[
        _ru_ahpe,
        _ru_aeqp,
        _ru_aheh,
    ],
)

_gnb0_smod = CommonUnit(
    lmp_connection=_bts_0_ssh_lmp_connection,
    capacity_units=[_gnb0_bbmod_bottom, _gnb0_bbmod_middle, _gnb0_bbmod_top],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH214540951",
    mac_addr="",
    slot_id="C2",
    pdu_port=_fpfh_pdu_zd08_31.pdu_ports[2],
)
_gnb1_smod = CommonUnit(
    lmp_connection=_bts_1_ssh_lmp_connection,
    capacity_units=[_gnb1_bbmod_bottom],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233304579",
    mac_addr="",
    slot_id="C1",
    pdu_port=_fpfh_pdu_zd08_31.pdu_ports[1],
)

_airscale_bts_0 = Airscale(common_units=[_gnb0_smod], product_code="473098A")

_airscale_bts_1 = Airscale(common_units=[_gnb1_smod], product_code="473098A")

_du_gnb_0 = DU(
    airscale=_airscale_bts_0,
    oam_ip=_bts_0_oam_network_address,
    instance_id=_bts_0_mrbtsid,
    global_bts_id=_bts_0_nrbtsid,
)

_du_gnb_1 = DU(
    airscale=_airscale_bts_1,
    oam_ip=_bts_1_oam_network_address,
    instance_id=_bts_0_mrbtsid,
    global_bts_id=_bts_0_nrbtsid,
)

_bts_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_bts_0_mrbtsid,
    global_bts_id=_bts_0_nrbtsid,
    dcap=_utf,
)

_bts_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_bts_1_mrbtsid,
    global_bts_id=_bts_1_nrbtsid,
    dcap=_utf,
)

_test_pc_bts_0 = TestPc(
    default_ssh_connection_details=_ssh_test_vm_0,
    connections=[
        Connection(
            device=_gnb0_smod,
            interface="eth1",
            interface_type="lmp",
        )
    ],
)

_test_pc_bts_1 = TestPc(
    default_ssh_connection_details=_ssh_test_vm_1,
    connections=[
        Connection(
            device=_gnb1_smod,
            interface="eth1",
            interface_type="lmp",
        )
    ],
)

_appsrv = TafUeAppServer(
    app_server_name="SKA-HC14-15",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user=_APP_SERVER_USER,
    password=_APP_SERVER_PASSWORD,
    expected_prompt=_EXPECTED_PROMPT,
)

_appsrv2 = TafUeAppServer(
    app_server_name="SKA-HC14s18-2",
    address="SKA-HC14s18-2.p00-hc14.ska-lab.nsn-rdnet.net",
    bind_interface_ip="10.84.169.51",
    user=_APP_SERVER_USER,
    password=_APP_SERVER_PASSWORD,
    expected_prompt=_EXPECTED_PROMPT,
)

_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appsrv2,
    binary_path="/data/data/com.nokia.android.application/",
)

_uepc_addr = "plkr-uepc-sg4-1.intra.noklab.net"
_uepc_user = "plkrsg4"
_uepc_pass = "Rz0dkiewk@2024"
_ue_1_adb_sn = "1b3a4ff3"
_uepc_ssh = SshServiceDetails(addr=_uepc_addr, username=_uepc_user, password=_uepc_pass)

_ue_1_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    proxy_mngr_port=_PROXY_MNGR_PORT,
    serial_number=_ue_1_adb_sn,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

_ue_1_at = TafUeAt(
    com_port="dynamic",
    serial_number=_ue_1_adb_sn,
    capabilities=["AT_UE"],
    ue_pc_address=_uepc_addr,
    ue_pc_login=_uepc_user,
    ue_pc_password=_uepc_pass,
    proxy_mngr_port=_PROXY_MNGR_PORT,
    data_transfer=[_iperf],
)

_ue_2_android = TafUeAndroid(
    ssh_connection_details=_uepc_ssh,
    ue_pc_address=_uepc_addr,
    proxy_mngr_port=_PROXY_MNGR_PORT,
    serial_number="0123456789ABCDEF",
    capabilities=["MTK_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

tl = TestLine(
    test_pc=_test_pc_bts_0,
    gnbs=[_bts_0, _bts_1],
    test_pcs=[_test_pc_bts_0, _test_pc_bts_1],
    ues=[_ue_1_android, _ue_1_at, _ue_2_android],
    attenuators=[_attenuator1],
    pdus=[_fpfh_pdu_zd09_43, _hpe_pdu_zd09],
    tl_cloud_topology="CLOUD_7_7_T09SK030",
)

__all__ = ["tl"]
