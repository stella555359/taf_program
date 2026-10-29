__maintainer__ = "5G SC QT"
__team__ = "5G QT"
__email__ = "I_SC_5G_QT_KRK@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-gnb-026.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="10.83.182.26",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.26", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.26", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
)


_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="sc5g-hub-008.sc5g.krk-lab.nsn-rdnet.net",
                username="ute",
                password="ute",
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-gnb-026.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
    mme_ip="10.10.40.100",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=60002,
    egate_port=60001,
)

_lteenb = RealEnb(airscale=_du, x2_link_addr="10.10.40.10")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKM01L_ABILM02B1",
)

__all__ = ["tl"]
