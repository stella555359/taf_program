# ##########################################################################################
#
#    7_20_UTE4GCLASSSV330  -  IV_PS_330  -  CV330
#
#    2024-07-04 09:46:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Alain Gotte"
__team__ = "MN RAN RD VRF NPS 1"
__email__ = "alain.gotte@nokia.com"

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
from taf.config.testline.flexi import Flexi
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

_du1_pdu_enb = FPFH(addr="10.28.5.225", login="admin", password="admin", port_numbers=[4])
_ru1_pdu_enb = FPFH(addr="10.28.5.222", login="admin", password="admin", port_numbers=[5])
_ru2_pdu_enb = FPFH(addr="10.28.5.222", login="admin", password="admin", port_numbers=[6])
_ru3_pdu_enb = FPFH(addr="10.28.5.211", login="admin", password="admin", port_numbers=[6])
_ru4_pdu_enb = FPFH(addr="10.28.4.16", login="admin", password="admin", port_numbers=[4])
_ru5_pdu_enb = FPFH(addr="10.28.4.16", login="admin", password="admin", port_numbers=[6])
_rmod_enb_2 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[5], radio_type="FRMA", ru_hw_group="NR_RADIO", serial_number="K9171625799"
)
_rmod_enb_1 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[6], radio_type="FRMA", ru_hw_group="NR_RADIO", serial_number="K9171625823"
)
_rmod_enb_3 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[6], radio_type="FRHC", ru_hw_group="NR_RADIO", serial_number="F7164312891"
)
_rmod_enb_5 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[4], radio_type="FXEB", ru_hw_group="NR_RADIO", serial_number="NK163703311"
)
_rmod_enb_4 = RU(
    pdu_port=_ru5_pdu_enb.pdu_ports[6], radio_type="FXEB", ru_hw_group="NR_RADIO", serial_number="NK164202775"
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="FBBC",
    hardware_version="101",
    product_code="472797A.101",
    rus=[_rmod_enb_4, _rmod_enb_5],
    serial_number="NK170430717",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="FBBC",
    hardware_version="101",
    product_code="472797A.101",
    rus=[_rmod_enb_3],
    serial_number="AS183320199",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_2, _fsp_enb_1],
    hardware_type="Flex",
    hardware_version="472181A",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[4],
    serial_number="F7163849213",
)
_smod_enb_1 = Flexi([_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=33005,
    instance_id=33005,
    oam_ip=NetworkAddress(v4="10.14.48.22"),
    rms=[_rmod_enb_3, _rmod_enb_4, _rmod_enb_5],
    system_module=_smod_enb_1,
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.218", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_enb, _ru1_pdu_enb, _ru2_pdu_enb, _ru3_pdu_enb, _ru4_pdu_enb, _ru5_pdu_enb]
_tl_cloud_topology = "CLOUD_SRAN_L_Flex_2xFlex_FRHC_2xFXEB_2xFRMA_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
