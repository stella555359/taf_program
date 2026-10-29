__maintainer__ = "Krystian Krakowski"
__team__ = "I_MN_RAN_RD_VRF_KRK_12"
__email__ = "I_MN_RAN_RD_VRF_KRK_12@internal.nsn.com"
__owner_email__ = "krystian.krakowski@nokia.com"

from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import FPFH
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GKRK2TL246.bcu3.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_pdu1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="10.253.167.10",
    login="admin",
    password="admin",
)
_pdus = [_pdu1]

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
    username="Nemuadmin",
    password="nemuuser",
)

_cu_gnb = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="192.168.255.129"),
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1746),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1746),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1746),
)

_abil_master_gnb = CapacityUnit(addr="192.168.253.20")

_du_common_unit_gnb = CommonUnit(
    pdu_port=_pdus[0].pdu_ports[1],
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[_abil_master_gnb],
    hardware_type="ASIB",
    hardware_version="A102",
)

_ru_gnb = RU(
    ru_hw_group="AHPF",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128",
        username="root",
    ),
    pdu_port=_pdus[0].pdu_ports[5],
    radio_type=RadioTypes.AHPF,
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])
_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb])

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
)

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABILB1_AHPF",
    pdus=_pdus,
)

__all__ = ["tl"]
