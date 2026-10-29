__maintainer__ = "SHI Kun"
__team__ = "MG_5G_NJN_UUF_PET"
__email__ = "I_5GASIR_UUF_PET@internal.nsn.com"
__owner_email__ = "kun.shi@nokia-sbell.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio, RealEnb, NetworkAddress
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, BlackBox


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.14.57", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="172.31.1.11",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.11", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lte_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.16.167", username="ute", password="ute"),
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_lte_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIA", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A102",
)

_lte_common_unit = CommonUnit(
    lmp_connection=_lte_lmp_connection,
    capacity_units=[_lte_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A102",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.16.168", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=BlackBox(addr="10.66.14.1", port_numbers=[8]), port_no=4001),
)

_airscale = Airscale(common_units=[_du_common_unit])

_airscale_enb = Airscale(common_units=[_lte_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_gnb = ClassicalBts(cu=_cu, dus=[_du])

_enb = RealEnb(system_module=_airscale_enb, oam_ip=NetworkAddress(v4="172.31.1.10"))

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.16.169", username="ute", password="ute"
    ),
    dir_path="/home/wts",
    cfg_filename="epcsim.cfg",
    mme_ip="172.31.1.1",
    mcc="460",
    mnc="2",
    tac=111,
    edaemon_port=60002,
    egate_port=60001,
)

tl = TestLine(
    test_pc=_test_pc,
    enbs=[_enb],
    gnbs=[_gnb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIBA102R_ABILA102B1",
)

__all__ = ["tl"]
