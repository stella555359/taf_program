__maintainer__ = "Magda Bielska"
__team__ = "MN RAN RD VRF WRO3 7"
__email__ = "magdalena.bielska@nokia.com"

from typing import Optional, List, Union
from enum import Enum
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import DU, CU, ClassicalBts
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import Gude
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine

from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.airscale import CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc, Connection

_pdu_1 = Gude(addr="10.42.168.168", port_numbers=[4, 3], model="EPC", version="8220-1")
_pdu_2 = Gude(addr="10.42.168.74", port_numbers=[5],model="EPC", version="8220-1")
_pdu_3 = Gude(addr="10.42.169.88", port_numbers=[1, 2, 3, 4, 5, 6, 7], model="EPC", version="8220-1")
_pdu_4 = Gude(addr="10.42.169.63", port_numbers=[8, 9], model="EPC", version="8220-1")

_pdus = [_pdu_1, _pdu_2, _pdu_3, _pdu_4]

_rmod_1 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHPMDG",
    serial_number="BL2344C66RY",
    pdu_port=_pdu_4.pdu_ports[8],
)
_rmod_2 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHPMDG",
    serial_number="BL2343C66BB",
    pdu_port=_pdu_3.pdu_ports[2],
)
_rmod_3 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHPMDG",
    serial_number="BL2344C66NX",
    pdu_port=_pdu_3.pdu_ports[1],
)
_rmod_4 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHEGG",
    serial_number="RW232200990",
    pdu_port=_pdu_3.pdu_ports[6],
)
_rmod_5 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHEGG",
    serial_number="K9252214053",
    pdu_port=_pdu_3.pdu_ports[7],
)
_rmod_6 = RU(
    ru_hw_group="FRMr6.2_4T4R",
    radio_type="AHEGG",
    serial_number="RW232200991",
    pdu_port=_pdu_4.pdu_ports[9],
)
_rmod_7 = RU(
    ru_hw_group="cMAAr7.1_32T32R",
    radio_type="AVQQ",
    serial_number="1M242100044",
    pdu_port=_pdu_3.pdu_ports[3],
)
_rmod_8 = RU(
    ru_hw_group="cMAAr6.1_32T32R_eCPRI",
    radio_type="AEQQ",
    serial_number="1M221913335",
    pdu_port=_pdu_3.pdu_ports[4],
)
_rmod_9 = RU(
    ru_hw_group="cMAAr6.1_32T32R_eCPRI",
    radio_type="AEQQ",
    serial_number="1M220620980",
    pdu_port=_pdu_3.pdu_ports[5],
)
_rmod_10 = RU(
    ru_hw_group="FRMr5.1_1_6T6R",
    radio_type="ARDA",
    serial_number="K9203323102",
    pdu_port=_pdu_2.pdu_ports[5],
)
_fsp_1 = CapacityUnit(
    addr="192.168.254.125",
    hardware_type="ABIO",
    serial_number="L1204806013",
    pdu_port=_pdu_1.pdu_ports[4],
    rus=[_rmod_7, _rmod_8, _rmod_9],
)
_fsp_2 = CapacityUnit(
    addr="192.168.254.127",
    hardware_type="ABIO",
    serial_number="L1204703440",
    pdu_port=_pdu_1.pdu_ports[4],
    rus=[_rmod_1, _rmod_2, _rmod_3],
)
_fsp_3 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIA",
    serial_number="L1163607861",
    pdu_port=_pdu_1.pdu_ports[4],
    rus=[_rmod_4, _rmod_5, _rmod_6],
)
_fsp_4 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    serial_number="DH195290546",
    pdu_port=_pdu_1.pdu_ports[3],
    rus=[_rmod_10],
)
_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1, _fsp_2, _fsp_3],
    pdu_port=_pdu_1.pdu_ports[4],
    hardware_type="ASIB",
    serial_number="L1182811228",
)
_fct_2 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_4],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIA",
    serial_number="L1163201126",
)

_smod_1 = Airscale([_fct_1])
_smod_2 = Airscale([_fct_2])

_enb_sbts_1 = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5, _rmod_6, _rmod_7, _rmod_8, _rmod_9],
    oam_ip=NetworkAddress("10.42.175.66"),
    instance_id=1318,
)
_enb_sbts_2 = RealEnb(
    system_module=_smod_2,
    rms=[_rmod_10],
    master=_enb_sbts_1,
)
_enb_sbts_1.slave = _enb_sbts_2


_test_pc_1 = TestPc(
    SshServiceDetails(addr="10.42.184.46", username="ute"),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            device=_enb_sbts_1.system_module.common_units[0],
            interface_type="lmp",
        ),
    ],
)

_test_pc_2 = TestPc(
    SshServiceDetails(addr="10.42.184.47", username="ute"),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            device=_enb_sbts_2.system_module.common_units[0],
            interface_type="lmp",
        ),
    ],
)

tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1, _test_pc_2],
    enbs=[_enb_sbts_1, _enb_sbts_2],
    pdus=_pdus,
)

__all__ = ["tl"]
