# Generated with TL configuration generator at 2023-09-04_11:08:02

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.82.28.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.82.28.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.28.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.48.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.50.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.82.30.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.48.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.82.30.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.82.30.12/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK012.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 81012
_gnb_global_bts_id = 81012

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

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232807079",
    product_code="475792A.102",
    # slot_id=SlotId.B6
)

gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223610014",
    product_code="475266A.104",
    # slot_id=SlotId.B4
)

gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIO",
    hardware_version="B.101",
    serial_number="L1223309970",
    product_code="475266B.101",
    # slot_id=SlotId.B5
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIM",
    hardware_version="A.101",
    serial_number="L1224401628",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300376",
    product_code="475295A.101",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH211600063",
    product_code="475295A.101",
)

gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300114",
    product_code="475295A.101",
)

gnb_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300120",
    product_code="475295A.101",
)

gnb_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300636",
    product_code="475295A.101",
)

gnb_radio_unit_5 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300112",
    product_code="475295A.101",
)

gnb_radio_unit_6 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300098",
    product_code="475295A.101",
)

gnb_radio_unit_7 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300102",
    product_code="475295A.101",
)

gnb_radio_unit_8 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300097",
    product_code="475295A.101",
)

gnb_radio_unit_9 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH212400132",
    product_code="475295A.101",
)

gnb_radio_unit_10 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH211600088",
    product_code="475295A.101",
)

gnb_radio_unit_11 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH223900251",
    product_code="475295A.101",
)

gnb_radio_unit_12 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH211600026",
    product_code="475295A.101",
)

gnb_radio_unit_13 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH221300877",
    product_code="475295A.101",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[
        gnb_radio_unit_0,
        gnb_radio_unit_1,
        gnb_radio_unit_2,
        gnb_radio_unit_3,
        gnb_radio_unit_4,
        gnb_radio_unit_5,
        gnb_radio_unit_6,
        gnb_radio_unit_7,
        gnb_radio_unit_8,
        gnb_radio_unit_9,
        gnb_radio_unit_10,
        gnb_radio_unit_11,
        gnb_radio_unit_12,
        gnb_radio_unit_13,
    ],
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
    v4="10.82.28.13/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.82.28.13/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK013.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 81013
_enb_global_bts_id = 81013

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIA",
    hardware_version="A.106",
    serial_number="DH204991814",
    product_code="473096A.106",
    # slot_id=SlotId.B2
)

enb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.105",
    serial_number="DH203390250",
    product_code="473096A.105",
    # slot_id=SlotId.B1
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0, enb_capacity_unit_1],
    hardware_type="ASIM",
    hardware_version="A.102",
    serial_number="L1230610668",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

enb_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300376",
    product_code="475295A.101",
)

enb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300102",
    product_code="475295A.101",
)

enb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300114",
    product_code="475295A.101",
)

enb_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300120",
    product_code="475295A.101",
)

enb_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300097",
    product_code="475295A.101",
)

enb_radio_unit_5 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.134", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300636",
    product_code="475295A.101",
)

enb_radio_unit_6 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.132", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300112",
    product_code="475295A.101",
)

enb_radio_unit_7 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH211600063",
    product_code="475295A.101",
)

enb_radio_unit_8 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300098",
    product_code="475295A.101",
)

enb_radio_unit_9 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.41.137", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH221300877",
    product_code="475295A.101",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_enb = RealEnb(
    rms=[
        enb_radio_unit_0,
        enb_radio_unit_1,
        enb_radio_unit_2,
        enb_radio_unit_3,
        enb_radio_unit_4,
        enb_radio_unit_5,
        enb_radio_unit_6,
        enb_radio_unit_7,
        enb_radio_unit_8,
        enb_radio_unit_9,
    ],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
)

__all__ = ["tl"]
