__maintainer__ = "Kamil Gorski"
__team__ = "MN RAN Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"
__owner_email__ = "kamil.gorski@nokia.com"


from taf.config.testline.testpc import TestPc
from taf.config.testline import DU
from taf.config.testline.gnb import CU
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import CommonUnit, Airscale, CapacityUnit
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.gnb import ClassicalBts
from taf.config.testline.pdu import FPFH, PduPort
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)

_pdu = FPFH(
    addr="10.253.166.17",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
    model="FPFH",
)

_secondary_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.178.45",
        username="ute",
        password="ute",
    )
)

_main_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.178.23",
        username="ute",
        password="ute",
    )
)

_common_unit_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)
_common_unit = CommonUnit(
    lmp_connection=_common_unit_lmp_connection,
    capacity_units=None,
    hardware_type="AMIA",
    pdu_port=PduPort(pdu=_pdu, port_no="1"),
)
_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)
_cu = CU(
    backhaul_site_oam_ip=None,
    oam_ssh_connection_details=None,
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

tl = TestLine(
    test_pc=_main_test_pc,
    test_pcs=[_main_test_pc, _secondary_test_pc],
    gnbs=[_classical_bts],
    pdus=[_pdu],
)

__all__ = ["tl"]
