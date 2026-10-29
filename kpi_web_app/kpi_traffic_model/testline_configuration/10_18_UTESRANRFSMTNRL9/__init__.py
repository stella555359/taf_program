__maintainer__ = "constantin.diaconu@nokia.com"
__owner__ = "constantin.diaconu@nokia.com"
__email__ = "constantin.diaconu@nokia.com"
import os
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import Gude
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.bts2g import Bts2G
from taf.config.testline.nb import NB
from taf.config.testline.ran import RNC
from taf.config.testline.gnb import DU
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.airscale import CommonUnit, CapacityUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import PDNAndroidDetails, TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.ue import TafUeAt
from taf.config.testline.optical_switch import Calient

_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.19.137", username="ute", password="UTE.debian12"
    ),
    connections=[NetworkAddress(v4="192.168.255.126")],
)

_test_pc_3 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.19.21", username="ute", password="UTE.debian12"
    ),
    connections=[NetworkAddress(v4="192.168.255.126")],
)

_pdu_1 = Gude("10.255.5.223", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")
_pdu_1.pdu_ports[3].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[5].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[9].contactor = "NORMALLY_CLOSED"

_pdu_2 = Gude("10.255.5.222", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")
_pdu_2.pdu_ports[1].contactor = "NORMALLY_CLOSED"
_pdu_2.pdu_ports[2].contactor = "NORMALLY_CLOSED"
_pdu_2.pdu_ports[3].contactor = "NORMALLY_CLOSED"
_pdu_2.pdu_ports[5].contactor = "NORMALLY_CLOSED"
_pdu_2.pdu_ports[10].contactor = "NORMALLY_CLOSED"

# Shared
_rmod_1 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AZHA.value,
    serial_number="RW191507788",
    pdu_port=_pdu_2.pdu_ports[10],
)

# Shared
_rmod_2 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AZHA.value,
    serial_number="RW191708315",
    pdu_port=_pdu_2.pdu_ports[3],
)

# Shared
_rmod_3 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AREA.value,
    serial_number="EA223454075",
    pdu_port=_pdu_2.pdu_ports[1],
)

# Dedicated BTS1
_rmod_4 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AREA.value,
    serial_number="EA191771025",
    pdu_port=_pdu_2.pdu_ports[2],
)

# Dedicated BTS2
_rmod_5 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AKQZ.value,
    serial_number="K9222903894",
    pdu_port=_pdu_2.pdu_ports[5],
)

_fsp_abio_bts1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204104699",
    rus=[_rmod_1, _rmod_2, _rmod_3],
)

_fsp_abip_bts2 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233201712",
    rus=[_rmod_1, _rmod_2, _rmod_3],
)

_fsp_abio_bts2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1223400373",
    rus=[_rmod_5],
)

_fct_asib_bts1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_abio_bts1],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1211205010",
    test_pc=_test_pc_1,
)

_fct_asim_bts2 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_abip_bts2, _fsp_abio_bts2],
    pdu_port=_pdu_1.pdu_ports[5],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="DH251432985",
    test_pc=_test_pc_3,
)

_smod_1 = Airscale([_fct_asib_bts1])
_smod_2 = Airscale([_fct_asim_bts2])

_enb_lte_1 = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_4],
    instance_id=621009,
    oam_ip=NetworkAddress(v4="10.0.70.9"),
    bcf_id="3009",
)

_test_pc_1.connections.append(
    Connection(
        interface="eth1",
        device=_enb_lte_1.system_module.common_units[0],
        interface_type="lmp",
    )
)

_enb_lte_2 = RealEnb(
    system_module=_smod_2,
    rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_5],
    instance_id=624009,
    oam_ip=NetworkAddress(v4="10.0.65.9"),
)

_test_pc_3.connections.append(
    Connection(
        interface="eth1",
        device=_enb_lte_2.system_module.common_units[0],
        interface_type="lmp",
    )
)

_bsc_bts1 = BSC(
    name="BSC",
    logging_ssh_connection_details=SshServiceDetails(
        addr="10.27.126.201", username="SYSTEM", password="SYSTEM"
    ),
)

tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1, _test_pc_3],
    enbs=[_enb_lte_1, _enb_lte_2],
    bscs=[_bsc_bts1],
    tl_cloud_topology="None",
)

RFS_TL_FLAGS = {
    "fail_if_unexpected_alarms": True,
    "fail_if_wrn_threshold": True,
}

__all__ = ["tl"]

