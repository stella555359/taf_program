# ##########################################################################################
#
#    7_20_UTE4GCLASSSV313  -  IV_PS_313  -  CV313
#
#    2024-01-02 17:31:09.152165:
#    __init__.py generator (version 2.0 of 02/12/2023).
#
# ##########################################################################################

__maintainer__ = ""
__team__ = "MN RAN Pz NPS SG2"
__email__ = "@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import Connection, TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, FPFH, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android
from collections import OrderedDict
from taf.config.testline.gnb.du import Cablink, Endpoint

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_du1_pdu_enb = FPFH(addr="10.28.1.106", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_enb = FPFH(addr="10.0.116.74", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_enb = FPFH(addr="10.0.116.75", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru7_pdu_enb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru8_pdu_enb = FPFH(addr="10.0.116.73", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru9_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_enb_6 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914834"
)
_rmod_enb_1 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="BL2138F1RWG"
)
_rmod_enb_5 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914833"
)
_rmod_enb_2 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="K9183800521"
)
_shared_rmod_8 = RU(
    pdu_port=_ru5_pdu_enb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="BL2120V0D4F"
)
_shared_rmod_7 = RU(
    pdu_port=_ru6_pdu_enb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="BL1923V0A8P"
)
_rmod_enb_4 = RU(
    pdu_port=_ru7_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914831"
)
_shared_rmod_9 = RU(
    pdu_port=_ru8_pdu_enb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="K9184615750"
)
_rmod_enb_3 = RU(
    pdu_port=_ru9_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="K9183800520"
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_9, _shared_rmod_8, _shared_rmod_7],
    serial_number="EA192071772",
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_5, _rmod_enb_6, _rmod_enb_4],
    serial_number="L1182601815",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2],
    serial_number="EA190473657",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_3, _fsp_enb_2, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[2],
    serial_number="RW192202804",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22297,
    instance_id=313,
    oam_ip=NetworkAddress(v4="10.14.48.23"),
    rms=[
        _rmod_enb_1,
        _rmod_enb_3,
        _rmod_enb_2,
        _rmod_enb_5,
        _rmod_enb_6,
        _rmod_enb_4,
        _shared_rmod_9,
        _shared_rmod_8,
        _shared_rmod_7,
    ],
    system_module=_smod_enb_1,
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.119", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_enb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
    _ru4_pdu_enb,
    _ru5_pdu_enb,
    _ru6_pdu_enb,
    _ru7_pdu_enb,
    _ru8_pdu_enb,
    _ru9_pdu_enb,
]
_tl_cloud_topology = "CLOUD_SRAN_L_ASIA_3xABIA_3xAHLBA_3xAHNA_3xAHFIB_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
