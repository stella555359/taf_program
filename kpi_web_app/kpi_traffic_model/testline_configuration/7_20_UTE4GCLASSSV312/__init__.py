# ##########################################################################################
#
#    7_20_UTE4GCLASSSV312  -  IV_PS_312  -  CV312
#
#    2023-11-17 11:31:31.476582:
#    __init__.py generator (version 1.0 of 21/09/2023).
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

_du1_pdu_enb = FPFH(addr="10.0.117.163", login="admin", password="admin", port_numbers=[3])
_ru1_pdu_enb = FPFH(addr="10.0.117.165", login="admin", password="admin", port_numbers=[3])
_ru2_pdu_enb = FPFH(addr="10.0.117.165", login="admin", password="admin", port_numbers=[5])
_ru3_pdu_enb = FPFH(addr="10.0.117.195", login="admin", password="admin", port_numbers=[3])
_shared_rmod_2 = RU(
    pdu_port = _ru1_pdu_enb.pdu_ports[3],
    radio_type="FRPD",
    ru_hw_group="NR_RADIO",
    serial_number="EA194510739",
)
_rmod_enb_1 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[5],
    radio_type="FXED",
    ru_hw_group="NR_RADIO",
    serial_number="F7172209594",
)
_rmod_enb_4 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[3],
    radio_type="FRHF",
    ru_hw_group="NR_RADIO",
    serial_number="F7184732976",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="104",
    product_code="473096A.104",
    rus=[_rmod_enb_1, _rmod_enb_4, _shared_rmod_2],
    serial_number="L1192400266",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[3],
    serial_number="L1190817401",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22287,
    instance_id=22287,
    oam_ip=NetworkAddress(v4="10.14.48.32"),
    rms=[_rmod_enb_1, _rmod_enb_4, _shared_rmod_2],
    system_module=_smod_enb_1,
)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.192", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_enb, _ru1_pdu_enb, _ru2_pdu_enb, _ru3_pdu_enb]
_tl_cloud_topology = "CLOUD_SRAN_L_ASIB_ABIA_FRPD_FXED_FRHF_UTECA"

tl = TestLine(
    core=_realcore,
    enbs=[_enb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
