__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, SWH

# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT295.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-093.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_bh_ip = "10.83.183.45"
_gnb_instance_id = 10295
_gnb_global_bts_id = 295
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="172.16.10.49")
_gnb_ru_hw_group = "AWEUA"

_gnb_oam_addr = NetworkAddress(
    v4="{}/23".format(_gnb_bh_ip),
    routing_v4=RoutingInformation(gateway="10.83.183.254"),
    vlan_id=503,
)
# eNB BH: 10.83.182.93

##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_bh_ip,
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
    backhaul_site_oam_ip=_gnb_oam_addr,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,  # replace if other than default
    s1u=_gnb_oam_addr,
    x2c=_gnb_oam_addr,
    x2u=_gnb_oam_addr,
)

_cu_gnb.sync = NetworkAddress(v6="", v4=_gnb_oam_addr.v4, vlan_id=0)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="192.168.253.20")
_abil_slave_gnb = CapacityUnit(addr="192.168.253.21")
_abil_loner_gnb = CapacityUnit(addr="192.168.253.22")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb, _abil_slave_gnb, _abil_loner_gnb],
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
    pdu_port=PduPort(pdu=SWH(addr="10.253.166.11", port_numbers=[1, 2]), port_no=1),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb])

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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AWEUA_TRUNK",
)

__all__ = ["tl"]
