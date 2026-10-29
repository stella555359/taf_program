__maintainer__ = "Jakub Siluch"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "jakub.siluch@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import RU
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit


# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT384.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="SC5G-eNB-053.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.83.183.134",
    v6="2a00:8a02:60:1c:0:0:1:384",
    vlan_id=503,
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AEUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
)
_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AEUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
)

_gnb_instance_id = 384
_gnb_global_bts_id = 384
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="172.22.48.162")
_gnb_ru_hw_group = "AEUB"

##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)
_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
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
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_du_capacity_unit = CapacityUnit(addr="fsp-1-1b", hardware_type="ABIL")
_du_capacity_unit_2 = CapacityUnit(addr="fsp-1-2b", hardware_type="ABIL")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_du_capacity_unit, _du_capacity_unit_2],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)


_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_1, _ru_2])

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

##############################################################


# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_enb],
    tl_cloud_topology="test",
)

__all__ = ["tl"]
