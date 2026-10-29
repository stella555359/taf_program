__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, SWH

# from taf.config.testline.pdu import FPFH

# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-cloudt088.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-093.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.88",
    routing_v4=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    vlan_id=503,
)

_s1u_oam_ip = NetworkAddress(
    v4="172.16.8.1",
    routing_v4=RoutingInformation(gateway="10.83.183.254", ip_prefix_length=23),
    vlan_id=2588,
)

_gnb_instance_id = 10088
_gnb_global_bts_id = 88
# _gnb_pdu = FPFH(port_numbers=[4], addr="10.253.166.62", login="admin", password="admin")
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.145")
_gnb_ru_hw_group = "AWEUA"

# eNB BH:  10.83.182.93

##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

##############################################################


# Important!: check and change below if other than default #

# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    s1u=_s1u_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="fsp1_c")  # 192.168.253.38

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    # pdu_port=_gnb_pdu,
    capacity_units=[_abil_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)

_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(pdu=SWH(addr="10.253.166.11", port_numbers=[1, 2]), port_no=2),
)  # B

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb], f1_m_ip_addr="10.83.182.88")

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKR_ABILB4_AWEUA",
)

__all__ = ["tl"]
