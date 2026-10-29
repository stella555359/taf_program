__maintainer__ = "Catalin Lazar"
__email__ = "iulian_catalin.lazar@nokia.com"

from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.pdu import Gude
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.bts2g import Bts2G
from taf.config.testline.ran import BSC

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(addr="10.5.20.20", username="ute"),
    connections=[NetworkAddress(v4="192.168.255.126")],
)
_bsc = BSC(
    name="BSC_ASTRA",
    logging_telnet_connection_details=TelnetConnectionDetails(
        addr="10.27.51.234", username="SYSTEM", password="SYSTEM"
    ),
)

_pdu_1 = Gude(
    addr="10.255.3.90",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8221-1",
)
_pdu_2 = Gude(
    addr="10.255.3.91",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8221-1",
)
_pdu_3 = Gude(
    addr="10.255.3.92",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8221-1",
)

_pdu_1.pdu_ports[7].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[8].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[9].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[10].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[11].contactor = "NORMALLY_CLOSED"
_pdu_1.pdu_ports[12].contactor = "NORMALLY_CLOSED"
_pdu_2.pdu_ports[7].contactor = "NORMALLY_OPENED"
_pdu_2.pdu_ports[8].contactor = "NORMALLY_OPENED"
_pdu_2.pdu_ports[9].contactor = "NORMALLY_OPENED"
_pdu_2.pdu_ports[10].contactor = "NORMALLY_OPENED"
_pdu_3.pdu_ports[4].contactor = "NORMALLY_OPENED"
_pdu_3.pdu_ports[5].contactor = "NORMALLY_OPENED"
_pdu_3.pdu_ports[6].contactor = "NORMALLY_OPENED"
_pdu_3.pdu_ports[9].contactor = "NORMALLY_OPENED"



_fsp_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="473096A.103",
    serial_number="EA185079804",
)

_fsp_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="475266A.107",
    serial_number="DH240906536",
)

_fsp_3 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="475792A.102",
    serial_number="L1251302722",
)


_fct_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1, _fsp_2, _fsp_3],
    pdu_port=_pdu_3.pdu_ports[9],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    serial_number="L1242501088",
)


_smod_1 = Airscale([_fct_1])

_rmod_1 = RU(
    ru_hw_group="FRMr2.3_3T6R_Vegas",
    radio_type=RadioTypes.FXJB.value,
    serial_number="K9170226115",
    pdu_port=_pdu_1.pdu_ports[10],
)

_rmod_2 = RU(
    ru_hw_group="FRMr4.3a_2T2R_Halo",
    radio_type=RadioTypes.FHDI.value,
    serial_number="EA181150274",
    pdu_port=_pdu_2.pdu_ports[9],
)

_rmod_3 = RU(
    ru_hw_group="FRMTDr5.1_1_4T4R",
    radio_type=RadioTypes.AZNA.value,
    serial_number="RW201700122",
    pdu_port=_pdu_3.pdu_ports[5],
)

_rmod_4 = RU(
    ru_hw_group="FRMr5.1_1_6T6R",
    radio_type=RadioTypes.ARGA.value,
    serial_number="K9221000282",
    pdu_port=_pdu_1.pdu_ports[12],
)

_rmod_5 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type=RadioTypes.AHEB.value,
    serial_number="EA194450550",
    pdu_port=_pdu_3.pdu_ports[4],
)

_rmod_6 = RU(
    ru_hw_group="FRMr5.1_1_6T6R",
    radio_type=RadioTypes.AREA.value,
    serial_number="EA212552305",
    pdu_port=_pdu_1.pdu_ports[11],
)

_rmod_7 = RU(
    ru_hw_group="FRMTDr5.1_1_4T4R",
    radio_type=RadioTypes.AZNA.value,
    serial_number="RW201700127",
    pdu_port=_pdu_3.pdu_ports[6],
)

_rmod_8 = RU(
    ru_hw_group="FRMTDr5.1_1_4T4R",
    radio_type=RadioTypes.AZNA.value,
    serial_number="RW201700129",
    pdu_port=_pdu_2.pdu_ports[7],
)

_rmod_9 = RU(
    ru_hw_group="FRMTDr5.1_1_4T4R",
    radio_type=RadioTypes.AZNA.value,
    serial_number="6Q191212121",
    pdu_port=_pdu_2.pdu_ports[10],
)

_rmod_10 = RU(
    ru_hw_group="FRMr5.1_1_2T4R",
    radio_type=RadioTypes.AHGA.value,
    serial_number="1M205017048",
    pdu_port=_pdu_2.pdu_ports[8],
)

_rmod_11 = RU(
    ru_hw_group="cMAAr6.1_32T32R_eCPRI",
    radio_type=RadioTypes.AEQW.value,
    serial_number="1M223512712",
    pdu_port=_pdu_1.pdu_ports[9],
)

_rmod_12 = RU(
    ru_hw_group="cMAAr6.1_32T32R_eCPRI",
    radio_type=RadioTypes.AEQW.value,
    serial_number="1M222318946",
    pdu_port=_pdu_1.pdu_ports[8],
)

_rmod_13 = RU(
    ru_hw_group="cMAAr6.1_32T32R_eCPRI",
    radio_type=RadioTypes.AEQW.value,
    serial_number="1M222643824",
    pdu_port=_pdu_1.pdu_ports[7],
)

_fsp_1.rus = [_rmod_1, _rmod_2, _rmod_5, _rmod_6]
_fsp_2.rus = [_rmod_3, _rmod_7, _rmod_8, _rmod_9, _rmod_10]
_fsp_3.rus = [_rmod_4, _rmod_5, _rmod_6, _rmod_11, _rmod_12, _rmod_13]

_enb_sbts = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5, _rmod_6, _rmod_7, _rmod_8, _rmod_9, _rmod_10, _rmod_11, _rmod_12, _rmod_13],
    oam_ip=NetworkAddress("10.15.236.169"),
    instance_id=10769,
)

_test_pc.connections.append(Connection(interface="eth1", device=_enb_sbts.system_module.common_units[0], interface_type="lmp"))

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    enbs=[_enb_sbts],
    tl_cloud_topology="CLOUD_SRAN_NLG_1769_1ASIM_1ABIA_1ABIO_1ABIP_1FXJB_1FHDI_4AZNA_1ARGA_1AEHB_1AREA_1AHGA_3AEQW",
    bscs=[_bsc],
)

__all__ = ["tl"]
