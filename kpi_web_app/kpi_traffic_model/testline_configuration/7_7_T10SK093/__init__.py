# Generated with TL configuration generator at 2025-09-09_10:26:28

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
    port_numbers=[1, 2],  # 1 ASIM 93, 2 ASIM 94
    addr="FPFH-ZI05-46-P10.p10-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_ru_pdu_fpfh2_ZI05 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],  # AHFII, AHLOB
    addr="FPFH-ZI05-34-P10.p10-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_ru_pdu_fpfh1_ZI06 = FPFH(
    port_numbers=[1, 3],  # AEHC 2x
    addr="fpfh-zi06-46-p10.p10-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_ru_pdu_fpfh2_ZI06 = FPFH(
    port_numbers=[1, 4, 5, 6],  # AEHC 642, 3x AVQQA
    addr="fpfh-zi07-01-p11.p11-leg.ska-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------


_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T10SK093-1.p10.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T10SK093-2.p10.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 84093
_gnb_0_global_bts_id = 84093

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
    v4="10.89.10.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.10.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
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
    v4="10.89.12.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.54.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.54.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.89.12.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.255.54.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.89.12.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.255.54.93/23",
    routing_v4=RoutingInformation(gateway="10.89.11.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
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
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    radio_type="AEHC",
    serial_number="AH231800642",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI06, port_no=1),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="AH245000608",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=4),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="AH244601005",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=6),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    radio_type="AEHC",
    serial_number="AH231800605",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh1_ZI06, port_no=3),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQA",
    serial_number="L1250806865",
    product_code="476596A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI06, port_no=4),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOB",
    serial_number="AH250102165",
    product_code="475910A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=5),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQA",
    serial_number="L1250402788",
    product_code="476596A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI06, port_no=5),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AVQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQA",
    serial_number="L1250710369",
    product_code="476596A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI06, port_no=6),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    radio_type="AEHC",
    serial_number="AH232100993",
    product_code="475124B.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh1_ZI06, port_no=1),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="K9245135162",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=2),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="K9245135267",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=1),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="BL2221N4061",
    product_code="475656A.101",
    pdu_port=PduPort(pdu=_ru_pdu_fpfh2_ZI05, port_no=3),
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIA",
    hardware_version="A.106",
    serial_number="DH204892506",
    product_code="473096A.106",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_10, _gnb_0_radio_unit_11, _gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233704817",
    product_code="475792A.102",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_10, _gnb_0_radio_unit_11, _gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233704815",
    product_code="475792A.102",
    slot_id=SlotId.B6,
    rus=[_gnb_0_radio_unit_4, _gnb_0_radio_unit_6, _gnb_0_radio_unit_7],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH221046246",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_5],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1250406992",
    product_code="475792A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_3, _gnb_0_radio_unit_8],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_3],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233302542",
    mac_addr="28:74:f5:09:ff:54",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
        _gnb_0_capacity_unit_4,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233302540",
    mac_addr="28:74:f5:09:ff:54",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=2
    ),  # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_7_7_T10SK093",
)

__all__ = ["tl"]
