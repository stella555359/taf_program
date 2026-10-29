__maintainer__ = "Durga Kant Yadav"
__owner_email__ = "durga.yadav@nokia.com"
__team__ = "RANPzBLRSG03CPKPI"
__email__ = "durga.yadav@nokia.com"

from typing import Optional, List, Union
from enum import Enum
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import Gude
from taf.config.testline.pdu import ATEN
from taf.config.testline.radio import RU
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine

from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.airscale import CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc

_test_pc_1 = TestPc(
    SshServiceDetails(addr="10.41.209.3", username="ute"),
    connections=[NetworkAddress(v4="192.168.255.126")],
)


_pdu_1 = Gude("10.41.155.41", [3], "MYCOMP", "8221-1")
_pdu_2 = Gude("10.41.155.42", [3], "MYCOMP", "8221-1")
# _pdu_3 = Gude("10.42.169.166", [2, 3, 4, 5, 10], "MYCOMP", "8221-1")

_fsp_1 = CapacityUnit(
    addr="192.168.255.1",
    hardware_type="ASIK",
    serial_number="DH212070710",
    product_code="474021A.103",
    pdu_port=_pdu_1.pdu_ports[3],
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIK",
    hardware_version="474021A.103",
    serial_number="DH212070710",
)

_smod_1 = Airscale([_fct_1])
# _smod_2 = Airscale([_fct_2])

_rmod_1 = RU(
    ru_hw_group="cMAA_Gen4.0_8T8R",
    serial_number="EA205151098",
    pdu_port=_pdu_2.pdu_ports[3],
    product_code="475130A.103",
    radio_type="AZQL",
)



_enb_sbts_1 = RealEnb(system_module=_smod_1, rms=[_rmod_1])


tl = TestLine(
    test_pc=_test_pc_1,
    # test_pcs=[_test_pc_1, _test_pc_2],
    enbs=[_enb_sbts_1],
)

__all__ = ["tl"]
