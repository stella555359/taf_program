# ##########################################################################################
#
#    7_20_UTE4GCLASSSV336  -  IV_PS_336  -  CV336
#
#    2023-12-04 15:57:10.051560:
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = "A NEZROUK"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "Abderrahmane.nezrouk@nokia.com"

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

_du1_pdu_enb = FPFH(addr="10.0.116.226", login="admin", password="admin", port_numbers=[4])
_ru1_pdu_enb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[5])
_ru2_pdu_enb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[6])
_ru3_pdu_enb = FPFH(addr="10.0.117.201", login="admin", password="admin", port_numbers=[6])
_shared_rmod_2 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[6],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2222N407P",
)
_shared_rmod_1 = RU(
    pdu_port = _ru1_pdu_enb.pdu_ports[5],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2234N41L4",
)
_shared_rmod_3 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[6],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2234N41KG",
)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="EA192178804"
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_1, _shared_rmod_3, _shared_rmod_2],
    serial_number="L1173619560",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1, _fsp_enb_2],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[4],
    serial_number="L1171800899",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22339,
    instance_id=22339,
    oam_ip=NetworkAddress(v4="10.14.48.118"),
    rms=[_shared_rmod_1, _shared_rmod_3, _shared_rmod_2],
    system_module=_smod_enb_1,
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.190", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_enb, _ru1_pdu_enb, _ru2_pdu_enb, _ru3_pdu_enb]
_tl_cloud_topology = "CLOUD_SRAN_L_ASIA_2xABIA_3xAHFII_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
