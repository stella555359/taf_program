# Generated with TL configuration generator at 2024-01-04_12:23:19

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"


from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.ue import Android
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU, CloudBts
from taf.config.testline import RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.pdu import FPFH
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="FPFH-PB03-46-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)


_ru_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="FPFH-PB03-31-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_ru_pdu_2 = ATEN(
    addr="aten-pb03-27-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    snmp_user={
        "userName": "administrator",
        "authKey": "password",
        "privKey": "password",
        "authProtocol": "MD5",
        "privProtocol": "AES",
    },
)


# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.45/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.45/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
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
    v4="10.83.252.45/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=541,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.253.214.45/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=543,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.83.182.45/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
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
        addr="7-7-UTE5GCLOUDT045.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 75045
_gnb_global_bts_id = 75045

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
    ru_hw_group="AWKUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.6",
        username="root",
        password="umniedziala",
    ),
    radio_type="AWKUA",
    serial_number="YK234900008",
    product_code="476237A.X21",
    pdu_port=PduPort(
        pdu=_ru_pdu_2, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="K9174801895",
    product_code="474216A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AWKUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.158",
        username="root",
        password="umniedziala",
    ),
    radio_type="AWKUB",
    serial_number="YK234700081",
    product_code="476238A.X21",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)
_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223704775",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_1],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223704781",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_0],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1204202773",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
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
# ---------------------------UE_CONFIGURATION---------------------

# AppServer CONFIGURATION

_appserver_ssh = SshServiceDetails(addr="10.83.249.134", username="5g", password="5g")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.83.249.164",
)

# UEs CONFIGURATION

_samsung_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-SC5G-PC78.sc5g.krk-lab.nsn-rdnet.net",
        username="pzkrk",
        password="NokiaBts2003",
    ),
    serial_number="R5CT910XVMT",
    server_dir="C:/pyro_server",
    # iperf_directory="/data/data/com.nokia.android.application/",
    python_path="C:/Users/pzkrk/AppData/Local/Programs/Python/Python36/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    service_call_attach="17",
    service_call_detach="17",
)


# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_2xABIO_AWKUB_AWKUA_AHFIB",
)

__all__ = ["tl"]
