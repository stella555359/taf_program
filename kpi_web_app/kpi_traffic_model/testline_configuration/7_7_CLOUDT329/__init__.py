__maintainer__ = "Jakub Czekaj"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "jakub.czekaj@nokia.com"


from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-CLOUDT329.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_ru_pdu = ATEN(addr="0.0.0.0", port_numbers=[1])


_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.54", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)


_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.183.79"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.79", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.79", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.83.183.79"),
    x2u=NetworkAddress(v4="10.83.183.79"),
    s1u=NetworkAddress(v4="10.83.183.79"),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3])

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-cloudt324.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/home/ute/epc_new",
    cfg_filename="sim1.cfg",
    mme_ip="10.253.165.74",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=10000,
    egate_port=60001,
)

_lteenb = NetworkAddress(v4="10.83.183.74")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    # enbs=[_lteenb],
    enbs=[],
    core=_core,
    tl_cloud_topology="test",
)

__all__ = ["tl"]
