# Generated with TL configuration generator at 2023-11-03_12:47:32

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
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CoreUnit, CapacityUnit, SlotId, TRSInterfaces
from taf.config.testline.pdu import PduPort, Pdu, FPFH, ATEN
import os
import yaml

# -------------------------PDU-------------------------------------
_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",
}

_gnb_pdu = FPFH(
    addr="FPFH-GF02-48-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1],
)

_ahca_pdu = FPFH(
    addr="fpfh-gf02-25-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1],
)

_aeud_pdu = ATEN(
    addr="aten-gf02-28-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[7],
    snmp_user=_snmp_user
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.128/23",
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
    v4="10.83.252.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=541,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.253.214.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=543,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.253.214.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=543,
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
        addr="7-7-UTE5GCLOUDT128.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_gnb_instance_id = 75128
_gnb_global_bts_id = 75128

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
     ru_hw_group="AEUD",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AEUD",
     serial_number="L1190301296",
     product_code="474611A.X31",
     pdu_port=PduPort(pdu=_aeud_pdu, port_no=7)
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="AHCA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala"),
     radio_type="AHCA",
     serial_number="AS210105161",
     product_code="473966A.101",
     pdu_port=PduPort(pdu=_ahca_pdu, port_no=1),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1213108378",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_0],
    )

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="DH200295168",
    product_code="473096A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_1],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1202703640",
    mac_addr="",
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=1),
    # trs_connections=[],
    slot_id=SlotId.C1,
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="475773A.101"
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

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.83.182.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.83.182.128/23",
    routing_v4=RoutingInformation(gateway="10.253.213.254", destIpAddr="10.83.249.104"),
    vlan_id=503,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT128.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute")
)

_enb_instance_id = 75128
_enb_global_bts_id = 75128

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

_enb_radio_unit_0 = RU(
     ru_hw_group="AHCA",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        username="root",
        password="umniedziala"),
     radio_type="AHCA",
     serial_number="AS210105161",
     product_code="473966A.101",
)

_enb_radio_unit_1 = RU(
     ru_hw_group="AEUD",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="root",
        password="umniedziala"),
     radio_type="AEUD",
     serial_number="L1190301296",
     product_code="474611A.X31",
)

_enb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1213108378",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_enb_radio_unit_1],
    )

_enb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="DH200295168",
    product_code="473096A.104",
    slot_id=SlotId.B1,
    rus=[_enb_radio_unit_0],
    )

_enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[_enb_capacity_unit_0, _enb_capacity_unit_1],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1202703640",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
)

_airscale_enb = Airscale(
    common_units=[_enb_common_unit_0],
    product_code="475773A.101"
    )

_enb = RealEnb(
    rms=[_enb_radio_unit_0, _enb_radio_unit_1],
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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_ABIA_ABIO_AHCA_AEUD_MRAT",
)

__all__ = ["tl"]
