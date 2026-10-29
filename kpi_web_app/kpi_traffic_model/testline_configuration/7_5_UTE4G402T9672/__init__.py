import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import HBTE, FPFH
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import DU

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    LicenseKeeper,
)

__maintainer__ = "Yin Chen"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_02_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_02@internal.nsn.com>"  # TL owner's team
__email__ = "yin.1.chen@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_pdu_1 = HBTE(addr="10.57.241.142", port_numbers=[1])

_fsp_1 = CapacityUnit(
    addr="192.168.253.18",
    hardware_type="FSIH",
    hardware_version="472568A.101",
    serial_number="EA1632B2514",
)

_fsp_2 = CapacityUnit(
    addr="192.168.253.19",
    hardware_type="FBIH",
    hardware_version="472568A.101",
    serial_number="L6144220364",
)

_fsp_3 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="FBIH",
    hardware_version="472568A.101",
    serial_number="L6144220368",
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.225.91", username="toor4nsn", password="oZPS0POrRieRtu"
)


_fct_1 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_fsp_1, _fsp_2, _fsp_3],
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="FSIH",
    hardware_version="472567A",
    serial_number="EA174503410",
)

_ru1_pdu = HBTE(addr="10.57.241.199", port_numbers=[3])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.FZNN,
    serial_number="10SHJ6TEA400540",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.254.129", port=2323
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
)

_ru2_pdu = FPFH(addr="10.57.241.199", port_numbers=[1])

_rmod_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.FZNN,
    serial_number="11CBB9WF4000049",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.254.130", port=2323
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
)

_ru3_pdu = FPFH(addr="10.57.241.199", port_numbers=[2])

_rmod_3 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.FZNN,
    serial_number="10NAA10D4000031",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.254.130", port=2323
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
)

_ru4_pdu = HBTE(addr="10.57.241.200", port_numbers=[8])

_rmod_4 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.FZNN,
    serial_number="11CBB9WG1000098",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.254.130", port=2323
    ),
    pdu_port=_ru4_pdu.pdu_ports[8],
)


# #RealEnb
_real_enb_pdu = FPFH(addr="10.57.241.142", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.225.91", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.225.91", username="Nemuadmin", password="nemuuser"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1, _common_unit_2])


_enb_sbts_1 = RealEnb(
    airscale=_real_enb,
    system_module=Airscale([_fct_1]),
    # rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_4],
    rms=[_rmod_2, _rmod_3, _rmod_4],
    oam_ip=NetworkAddress("10.57.225.91"),
    instance_id=9672,
    global_bts_id=9672,
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.96", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_enb_sbts_1],
)


tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    tl_cloud_topology="CLOUD_SRAN_L_1FSIH_4FZNN",
    test_pcs=[_host],
)
