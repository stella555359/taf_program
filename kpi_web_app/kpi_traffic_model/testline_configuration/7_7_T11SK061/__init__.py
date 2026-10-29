__maintainer__ = "Paulina Jedras, Piotr Brzezicki"
__team__ = "MN RAN RD VRF KRK 6"
__email__ = "paulina.jedras@nokia.com, piotr.brzezicki@nokia.com"

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
    CapacityUnit,
    SlotId,
)
from taf.config.testline.pdu import PduPort, FPFH
from taf.config.testline.lmi import SerialOverTcp, Remote

from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAt,
    PluginAtClassType,
)

# ------------------------PDU_CONFIGURATION------------------------

_pdu_fpfh_zi13_46 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zi13-46-p06.p06-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu_fpfh_zi13_16 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-zi13-16-p06.p06-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu_fpfh_zi10_01 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-zi10-01-p06.p06-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu_fpfh_zg10_46 = FPFH(
    port_numbers=[5, 6],
    addr="fpfh-zg10-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu_fpfh_zg12_48 = FPFH(
    port_numbers=[4],
    addr="fpfh-zg12-48-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNBs CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK061-1.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK061-2.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 81061
_gnb_0_global_bts_id = 81061

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.119",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0_secondary.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.61/23",
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
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.82.28.61/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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

_serviceuser_default_password = "Pl(FzaYj5~c5;q"

_ru_avha_206 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AVHA",
    serial_number="L1251001206",
    product_code="476542A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi10_01, port_no=1),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.41.64"), port=5001)]
    ),
)

_ru_ahlob_607 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHLOB",
    serial_number="AH243007607",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=4),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.31"), port=5001)]
    ),
)

_ru_awkud_726 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AWKUD",
    serial_number="AH243521726",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_pdu_fpfh_zg10_46, port_no=5),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.11.71"), port=5001)]
    ),
)

_ru_awkud_963 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AWKUD",
    serial_number="AH244716963",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_pdu_fpfh_zg10_46, port_no=6),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.11.70"), port=5001)]
    ),
)

_ru_ahfii_164 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHFII",
    serial_number="K9244348164",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_16, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.24"), port=5001)]
    ),
)

_ru_avha_218 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AVHA",
    serial_number="L1251001218",
    product_code="476542A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi10_01, port_no=2),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.41.65"), port=5001)]
    ),
)

_ru_awkud_967 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AWKUD",
    serial_number="AH244716967",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_pdu_fpfh_zg12_48, port_no=4),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.11.72"), port=5001)]
    ),
)

_ru_ahlob_865 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHLOB",
    serial_number="AH242902865",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=6),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.23"), port=5001)]
    ),
)

_ru_ahlob_823 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHLOB",
    serial_number="AH242902823",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=5),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.22"), port=5001)]
    ),
)

_ru_avha_097 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AVHA",
    serial_number="L1250304097",
    product_code="476541A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi10_01, port_no=3),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.41.63"), port=5001)]
    ),
)

_ru_ahfii_00w = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHFII",
    serial_number="BL2214N400W",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_16, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.26"), port=5001)]
    ),
)

_ru_ahfii_045 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password=_serviceuser_default_password,
    ),
    radio_type="AHFII",
    serial_number="BL2220N4045",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_16, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.14.25"), port=5001)]
    ),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1204002974",
    product_code="474020B.102",
    slot_id=SlotId.B1,
    rus=[_ru_ahlob_607, _ru_ahlob_823],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1213606688",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_ru_ahlob_865],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223610016",
    product_code="475266A.104",
    slot_id=SlotId.B3,
    rus=[_ru_ahfii_00w, _ru_ahfii_045, _ru_ahfii_164],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232807096",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[_ru_avha_206, _ru_avha_218, _ru_avha_097],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232807098",
    product_code="475792A.102",
    slot_id=SlotId.B5,
    rus=[_ru_awkud_963, _ru_awkud_967],
)

_gnb_0_capacity_unit_5 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233701300",
    product_code="475792A.102",
    slot_id=SlotId.B6,
    rus=[_ru_awkud_726],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233304585",
    mac_addr="28:74:f5:0a:1c:09",
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=1),
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_3,
        _gnb_0_capacity_unit_4,
        _gnb_0_capacity_unit_5,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233304584",
    mac_addr="28:74:f5:0a:1c:09",
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=2),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
    product_code="475773A",
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

_test_pc_gnb_0_secondary.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[1],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------ENB CONFIGURATION------------------------

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK061-3.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)


_enb_0_instance_id = 81023
_enb_0_global_bts_id = 81023

_enb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb_0.default_ssh_connection_details,
)

_enb_0_oam_ip = NetworkAddress(
    v4="10.82.28.23/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.23/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203893078",
    product_code="473096A.105",
    slot_id=SlotId.B1,
    rus=[_ru_ahfii_164, _ru_ahfii_045],
)

_enb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203893080",
    product_code="473096A.105",
    slot_id=SlotId.B2,
    rus=[_ru_ahfii_00w],
)

_enb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203893096",
    product_code="473096A.105",
    slot_id=SlotId.B3,
    rus=[_ru_ahlob_865, _ru_ahlob_823, _ru_ahlob_823],
)

_enb_0_common_unit_0 = CommonUnit(
    lmp_connection=_enb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _enb_0_capacity_unit_0,
        _enb_0_capacity_unit_1,
        _enb_0_capacity_unit_2,
    ],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH211572640",
    mac_addr="00:77:e4:5f:94:1",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_pdu_fpfh_zi13_46, port_no=3),
)

_enb_0_airscale = Airscale(
    common_units=[_enb_0_common_unit_0],
    product_code="475773A.101",
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

# ------------------------UEs CONFIGURATION------------------------

_appsrv = TafUeAppServer(
    app_server_name="SKA-HC14-15",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
    expected_prompt="\~\\$",
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appsrv,
    interval=1,
    binary_path="/cygdrive/c/iperf/",
    server_close_delay="100",
    version=2,
    dt_from_uepc=True,
    interface_name="Cellular",
)


_ue_1_quectel = TafUeAt(
    com_port="6",
    imei="861782060005650",
    capabilities=["REAL_QUECTEL_UE"],
    ue_pc_address="PLKR-SG07-39.intra.noklab.net",
    ue_pc_login="pzkrk",
    ue_pc_password="NokiaBts2003",
    ue_pc_expected_prompt="pzkrk@PLKR-SG07-39$",
    data_transfer=[_data_transfer_iperf],
    proxy_mngr_port=9955,
    ueproxy_force_release=False,
    class_name=PluginAtClassType.quectel,
)

_ue_1_quectel.ue_type = "quectel"

# ------------------------TL CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary, _test_pc_enb_0],
    ues=[_ue_1_quectel],
    tl_cloud_topology="CLOUD_7_7_T11SK061",
)

__all__ = ["tl"]
