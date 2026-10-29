# Generated with TL configuration generator at 2023-08-11_09:24:35

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
from taf.config.testline.pdu import PduPort, Pdu, FPFH
import os
import yaml

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.82.28.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.82.28.14/23",
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
    v4="10.82.28.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.48.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.50.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.82.30.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.48.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.82.30.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.82.30.14/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK014.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 81014
_gnb_global_bts_id = 81014

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

gnb_capacity_unit_0 = CapacityUnit(addr="192.168.255.129", hardware_type="ASOE")

_pdu_gnb = FPFH(
    addr="10.255.41.1",
    login="admin",
    password="admin",
    port_numbers=[1],
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    pdu_port=PduPort(pdu=_pdu_gnb, port_no=1),
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA214652464",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300233",
    product_code="475295A.101",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300223",
    product_code="475295A.101",
)

gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300225",
    product_code="475295A.101",
)

gnb_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300234",
    product_code="475295A.101",
)

gnb_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300230",
    product_code="475295A.101",
)

gnb_radio_unit_5 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300215",
    product_code="475295A.101",
)

gnb_radio_unit_6 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300236",
    product_code="475295A.101",
)

gnb_radio_unit_7 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="APHG",
    serial_number="NH225300108",
    product_code="475295A.101",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="N/A")

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

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
)

__all__ = ["tl"]
