__maintainer__ = "Daniel Wenecki"
__team__ = ""
__email__ = "daniel.wenecki@.nokia.com"
__owner_email__ = "daniel.wenecki@.nokia.com"

import os

from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.ue import Android
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.enb import RealEnb
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
        addr="sc5g-enb-327.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.183.77"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.77", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.77", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.83.183.77"),
    x2u=NetworkAddress(v4="10.83.183.77"),
    s1u=NetworkAddress(v4="10.83.183.77"),
)


_ru_pdu = ATEN(addr="0.0.0.0", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.151", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.152", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.153", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)


_cu.mplane_prefix = "23"
_cu.mplane_gw = "10.83.183.254"
_cu.mplane_id = "0.0.0.0"

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A101B1"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3])

_bts = ClassicalBts(cu=_cu, dus=[_du])


_lteenb = NetworkAddress(v4="10.83.183.77")


tl = TestLine(
    test_pc=_test_pc, gnbs=[_bts], enbs=[_lteenb], tl_cloud_topology="conf-class05"
)

__all__ = ["tl"]
