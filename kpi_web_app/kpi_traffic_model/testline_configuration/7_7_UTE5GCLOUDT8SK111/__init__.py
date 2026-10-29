__maintainer__ = "Mateusz Iwankiewicz"
__team__ = "I_MN_RAN_PZ_KRK_SG_8_GMS"
__email__ = "I_MN_RAN_PZ_KRK_SG_8@internal.nsn.com"
__owner_email__ = "mateusz.iwankiewicz@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, RadioTypes
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
from taf.config.testline.lmi import SerialOverHost, Local
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


cfg_dir = os.path.dirname(os.path.abspath(__file__))

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg06-31-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg05-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg04-46-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_3 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zh06-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_4 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg06-31-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_5 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg06-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK111-1.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK111-2.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 79111
_gnb_0_global_bts_id = 79111

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0_secondary.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.152.111/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50Y2",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_4, port_no=3),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM42')]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    radio_type="AWKUD",
    serial_number="AH244716948",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_ru_pdu_5, port_no=1),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    radio_type="AWKUD",
    serial_number="AH244716949",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_ru_pdu_4, port_no=6),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    radio_type="AEHC",
    serial_number="AH231800658",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=5),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM37')]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    radio_type="AEHC",
    serial_number="AH231800645",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=6),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM36')]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AWKUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    radio_type="AWKUD",
    serial_number="AH244201878",
    product_code="476240A.102",
    pdu_port=PduPort(pdu=_ru_pdu_5, port_no=2),
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50XX",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=2),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-tp-ue15.p08.ska-lab.nsn-rdnet.net',
    #                                                                 username='user-lab0', password='Bts2003')),
    #    uart_mapping=[Local(port='COM20')]
    # )
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50Y9",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_4, port_no=4),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM33')]
    # )
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    radio_type="AEHC",
    serial_number="AH231800610",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=1),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM38')]
    # )
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHFII",
    serial_number="K9245113271",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=4),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM41')]
    # )
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHFII",
    serial_number="BL2227N40LU",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=3),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM39')]
    # )
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    radio_type="AHFII",
    serial_number="BL2317N4500",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=2),
    # lmi=SerialOverHost(
    #    host=TestPc(default_ssh_connection_details=SshServiceDetails(addr='plkr-sc5g-pc85.p08.ska-lab.nsn-rdnet.net', username='pzkrk', password='NokiaBts2003')),
    #    uart_mapping=[Local(port='COM40')]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1222905787",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_8],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1190102692",
    product_code="474020A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_10, _gnb_0_radio_unit_11],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="L1214902977",
    product_code="475266A.103",
    slot_id=SlotId.B6,
    rus=[_gnb_0_radio_unit_1],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1195001926",
    product_code="474020A.102",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1190102726",
    product_code="474020A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_7],
)

_gnb_0_capacity_unit_5 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1224003730",
    product_code="475266A.104",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_2, _gnb_0_radio_unit_5],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_2,
        _gnb_0_capacity_unit_5,
    ],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1223402792",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_3,
        _gnb_0_capacity_unit_4,
    ],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1241108617",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
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

# ------------------------GNB0_CONFIGURATION TL 8SK113------------------------

_test_pc_gnb_113 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK113-1.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id113 = 79113
_gnb_0_global_bts_id113 = 79113

_gnb_0_primary_ssh_lmp_connection113 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_113.default_ssh_connection_details,
)

_gnb_0_oam_ip113 = NetworkAddress(
    v4="10.84.152.113/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1m_ip113 = NetworkAddress(
    v4="10.84.152.113/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1c_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_f1u_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2c_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2u_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1c_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnc_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnu_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngc_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngu_ip113 = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_oam_http_connection113 = HttpConnectionDetails(
    addr=_gnb_0_oam_ip113.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0_113 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip113,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection113,
    oam_http_connection_details=_gnb_0_oam_http_connection113,
    f1m=_gnb_0_f1m_ip113,
    f1c=_gnb_0_f1c_ip113,
    f1u=_gnb_0_f1u_ip113,
    x2c=_gnb_0_x2c_ip113,
    x2u=_gnb_0_x2u_ip113,
    s1c=_gnb_0_s1c_ip113,
    s1u=_gnb_0_s1u_ip113,
    xnc=_gnb_0_xnc_ip113,
    xnu=_gnb_0_xnu_ip113,
    ngc=_gnb_0_ngc_ip113,
    ngu=_gnb_0_ngu_ip113,
    instance_id=_gnb_0_instance_id113,
    global_bts_id=_gnb_0_global_bts_id113,
)

_gnb_0_radio_unit_0_113 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="K9245113271",
    product_code="475656A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1_113 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50Y2",
    product_code="475910A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2_113 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50XX",
    product_code="475910A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3_113 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="BL2228N410V",
    product_code="475656A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4_113 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="BL2317N4500",
    product_code="475656A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_5_113 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="BL2244D50Y9",
    product_code="475910A.101",
    # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0_113 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="K9173842014",
    product_code="473096A.103",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_1_113, _gnb_0_radio_unit_2_113, _gnb_0_radio_unit_5_113],
    )

_gnb_0_capacity_unit_1_113 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="EA183942878",
    product_code="473096A.103",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_3_113, _gnb_0_radio_unit_4_113],
    )

_gnb_0_capacity_unit_2_113 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1171720871",
    product_code="473096A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0_113],
    )

_gnb_0_common_unit_0_113 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection113,
    capacity_units=[_gnb_0_capacity_unit_0_113, _gnb_0_capacity_unit_1_113, _gnb_0_capacity_unit_2_113],
    hardware_type="ASIA",
    hardware_version="A.203",
    serial_number="AH184701833",
    mac_addr="78:f9:b4:03:7a:61",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale_113 = Airscale(
    common_units=[_gnb_0_common_unit_0_113],
    product_code="473098A",
    )

_du_gnb_0_113 = DU(
    airscale=_gnb_0_airscale_113,
    oam_ip=_gnb_0_oam_ip113,
    f1_m_ip_addr=_gnb_0_f1m_ip113,
    f1_c_ip_addr=_gnb_0_f1c_ip113,
    f1_u_ip_addr=_gnb_0_f1u_ip113,
    f1_m_cu=_gnb_0_f1m_ip113,
    f1_c_cu=_gnb_0_f1c_ip113,
    f1_u_cu=_gnb_0_f1u_ip113,
    instance_id=_gnb_0_instance_id113,
    global_bts_id=_gnb_0_global_bts_id113,
    )

_gnb_0_113 = ClassicalBts(
    cu=_cu_gnb_0_113,
    dus=[_du_gnb_0_113],
    instance_id=_gnb_0_instance_id113,
    global_bts_id=_gnb_0_global_bts_id113,
)

#-----------------------------------------------------------

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

# ------------------------TL_CONFIGURATION------------------------

_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_0_113],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_7_7_T8SK111",
)

__all__ = ["tl"]
