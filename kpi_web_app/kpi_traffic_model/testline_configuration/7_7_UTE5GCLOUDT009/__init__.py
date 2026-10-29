__maintainer__ = "Piotr Banasik"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "piotr.banasik@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline import ClassicalBts, DU, RU, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT009.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)
_abio1_du1 = CapacityUnit(
    addr="192.168.253.37", hardware_type="ABIO", serial_number="L1204301234"
)
_abio2_du1 = CapacityUnit(
    addr="192.168.253.38", hardware_type="ABIO", serial_number="L12042006256"
)
_abio3_du1 = CapacityUnit(
    addr="192.168.253.39", hardware_type="ABIO", serial_number="L1204008377"
)

_asib_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.83.182.9",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="7-7-UTE5GCLOUDT4SK009.sc5g.krk-lab.nsn-rdnet.net",
            username="ute",
            password="ute",
        ),
    ),
    hardware_type="ASIB",
    serial_number="L1213105584",
    capacity_units=[_abio1_du1, _abio2_du1, _abio3_du1],
)
_ru_du1 = RU(
    ru_hw_group="hw_group",
    serial_number="CV193300877",
    radio_type="AEQN",
)
_du1 = DU(
    Airscale(common_units=[_asib_du1]),
    rus=[_ru_du1],
    f1_m_ip_addr=NetworkAddress(v4="10.83.182.9"),
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.182.9/23"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.9", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.83.182.9"),
    x2u=NetworkAddress(v4="10.83.182.9"),
    s1u=NetworkAddress(v4="10.83.182.9"),
)
_gnb = ClassicalBts(
    dus=[_du1],
    cu=_cu,
    instance_id=75009,
    global_bts_id=75009,
)
_enb = RealEnb(
    oam_ip=NetworkAddress(v4="10.83.182.202"),
    instance_id=75202,
    global_bts_id=75202,
    x2_link_addr=NetworkAddress(v4="10.83.182.202"),
)
_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.177.195",
        username="user-lab0",
        password="Bts2003",
    ),
    connections=[
        NetworkAddress(v4="10.83.177.195"),
    ],
)
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_gnb],
    test_pcs=[_lss],
    enbs=[_enb],
)
__all__ = ["tl"]
