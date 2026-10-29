# Generated with TL configuration generator at 2022-05-23_10:16:43

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAndroid,
    Android,
    Connection,
)

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import Android
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import HPE

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
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
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.83.183.76",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT326.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 75326
_gnb_global_bts_id = 75326

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
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

gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.102",
    serial_number="L1213010213",
    product_code="474824A.102",
    # slot_id=SlotId.B1
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1201000223",
    mac_addr="00:77:e4:05:a7:b9",
    trs_connections=[TRSInterfaces.EIF1],
    # slot_id=SlotId.C1,
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[],
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

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.83.183.120",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.83.183.120",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT370.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 75370
_enb_global_bts_id = 75370

enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203791393",
    product_code="473096A.105",
    slot_id=SlotId.B4,
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="DH210566338",
    mac_addr="00:77:e4:49:36:a5",
    trs_connections=[TRSInterfaces.EIF1],
    # slot_id=SlotId.C2,
)

enb_radio_unit_0 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129", username="root", password="umniedziala"
    ),
    radio_type="AHHB",
    serial_number="EA214452284",
    product_code="474252A.102",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_enb = RealEnb(
    rms=[enb_radio_unit_0],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------------UE_CONFIGURATION------------------------

# TafUeAndroid
_realcore_appsrv = TafUeAppServer(
    app_server_name="realcore",
    address="10.83.249.130",
    bind_interface_ip="10.83.249.189",
    user="5g",
    password="5g",
)

_iperf_ue_sa = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_realcore_appsrv,
    # binary_path='/data/data/com.nokia.android.application/',
    interval=1,
    # server_close_delay=50
)

_android_ue_1 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-DMRS-UE4.intra.noklab.net",
        username="PLKR-DMRS-UE4+user-lab0",
        password="Bts2003",
    ),
    ue_pc_address="PLKR-DMRS-UE4.intra.noklab.net",
    serial_number="99b05df",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf_ue_sa],
    network_mode_switch_method="ADB",
)

# AppServer CONFIGURATION
_appserver_ssh = SshServiceDetails(addr="10.83.249.130", username="5g", password="5g")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.83.249.189",
)

# UE CONFIGURATION
_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-DMRS-UE4.intra.noklab.net",
        username="PLKR-DMRS-UE4+user-lab0",
        password="Bts2003",
    ),
    serial_number="99b05df",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

# ------------------------PDU_CONFIGURATION------------------------

_pdu = HPE(
    addr="phpg2-gb03.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[18],
    snmp_user={
        "userName": "user-lab0",
        "authKey": "NokiaBts2003",
        "privKey": "NokiaBts2003",
        "authProtocol": "MD5",
        "privProtocol": "DES",
    },
)

# ------------------------TL_CONFIGURATION------------------------

_attenuator = RadioRack(
    ip_addr="10.253.176.228", port=50000, attenuation_port_numbers=range(1, 17)
)

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIBL_ABINB1_APHG",
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    ues=[_android_ue_1],
    pdus=[_pdu],
    attenuator=_attenuator,
)

__all__ = ["tl"]
