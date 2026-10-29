__maintainer__ = "raluca-elena.butcovan@nokia.com"
__owner__ = "raluca-elena.butcovan@nokia.com"
__email__ = "raluca-elena.butcovan@nokia.com"

import os
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.pdu import Gude, FPFH, PSU
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.airscale import CommonUnit, CapacityUnit, CoreUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import DU
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline import PDNAndroidDetails, TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.ue import TafUeAt
from taf.config.testline.lmi import SerialOverHost,SerialOverTcp,Local, Remote


_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.19.26", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.126")],
)

_pdu_1 = Gude(
    "10.255.2.58",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8220-1",
)
_pdu_1.pdu_ports[8].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[9].contactor = "NORMALLY_CLOSED"


_pdu_2 = Gude(
    "10.255.2.57",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8220-1",
)
_pdu_2.pdu_ports[7].contactor = "NORMALLY_CLOSED"



_rmod_1 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AXEGHA.value,
    serial_number="L1260701715",
    pdu_port=_pdu_1.pdu_ports[8],
)

_rmod_2 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AXEGHA.value,
    serial_number="L1260900377",
    pdu_port=_pdu_1.pdu_ports[9],
)


_fsp_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="475266B.101",
    serial_number="L1223402766",
    rus=[_rmod_1, _rmod_2],
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_2.pdu_ports[7],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1250803243",
    test_pc=_test_pc_1,
)


_smod_1 = Airscale([_fct_1])

_enb_SBTS = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1, _rmod_2],
    instance_id=621001,
    oam_ip=NetworkAddress("10.0.69.202"),
)
_test_pc_1.connections.append(
    Connection(
        interface="eth1",
        device=_enb_SBTS.system_module.common_units[0],
        interface_type="lmp",
    )
)


tl = TestLine(
    test_pc=_enb_SBTS,
    test_pcs=[_test_pc_1],
    enbs=[_enb_SBTS],
    tl_cloud_topology="CLOUD_HRAN_RFS_MTNRL1",
)


RFS_TL_FLAGS = {
    "fail_if_unexpected_alarms": True,
    "fail_if_wrn_threshold": True,
    "POWER_ON_FLAG": True,
    "USER_RTWP_CHECK": False,
    "USER_STOP_AND_FIX": False,
    "USER_STOP_AND_FIX_BLOCK_TEST": False,
    "USER_DCAP_TRACE_COLLECT": False,
    "USER_DCAP_TRACE_COLLECT_Master": True,
    "USER_DCAP_TRACE_COLLECT_Slave": True,
    "USER_RSI_INFO_COLLECT": True,
    "USER_SCF_VALIDATION_CHECK": False,
    "NETACT_CHECK": False,
#    "RF_DIAGNOSTIC_CARD_CUSTOM_YAML": "/home/ute/testline_configuration/10_18_UTESRANRFSMTNRL69/MTNRL1_custom_rmod_setup.yaml",
}

__all__ = ["tl"]
