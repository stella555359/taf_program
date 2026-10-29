__maintainer__ = "Jakub Kupiec"
__team__ = "5G_PZ_MMW_KRK_4_SG"
__email__ = "jakub.kupiec@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RUExtension
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb

# The most commonly used testline configuration

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDTSK004.ska.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="ska-001-ute.ska.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = NetworkAddress(v4="10.44.3.99")
_gnb_instance_id = 10074
_gnb_global_bts_id = 4
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.145")
_gnb_ru_hw_group = "AEUB"

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
)

# Test PCs section

_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="192.168.253.20")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)

_ru_ext0 = RUExtension(
    radio_type="FA3UA", serial_number="L1201007250", product_code="474608A.103"
)

_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(pdu=ATEN(addr="", port_numbers=[3]), port_no=3),
    ru_extensions=[_ru_ext0],
    radio_type="AEUB",
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb])

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

x2_link_addr_enb = NetworkAddress(v4="10.44.3.65")

_lteenb = RealEnb(airscale=_airscale_gnb, x2_link_addr=x2_link_addr_enb)

# Testline section

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_lteenb],
    test_pcs=[_test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEUB",
)

__all__ = ["tl"]
