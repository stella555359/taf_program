# ##########################################################################################
#
#    7_20_UTE4GCLASSSV580  -  IV_PS_580  -  CV580
#
#    2023-11-20 14:17:32.670592:
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

# ##############################################################################
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ##############################################################################

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_du1_pdu_enb = FPFH(addr="10.0.96.95", login="admin", password="admin", port_numbers=[1])
_ru1_pdu_enb = FPFH(addr="10.0.97.67", login="admin", password="admin", port_numbers=[1])
_ru2_pdu_enb = FPFH(addr="10.28.1.111", login="admin", password="admin", port_numbers=[6])
_ru3_pdu_enb = FPFH(addr="10.28.1.109", login="admin", password="admin", port_numbers=[1])
_shared_rmod_3 = RU(
    pdu_port = _ru1_pdu_enb.pdu_ports[1],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="BL2012V092G",
)
_shared_rmod_2 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[6],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="BL1945V00JO",
)
_shared_rmod_1 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[1],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="K9182845211",
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_1, _shared_rmod_2, _shared_rmod_3],
    serial_number="L1173619631",
)
_fsp_enb_2 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="L1173606476"
)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="K9172606376"
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_3, _fsp_enb_2, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[1],
    serial_number="L1173502440",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22131,
    instance_id=580,
    oam_ip=NetworkAddress(v4="10.14.49.79"),
    rms=[_shared_rmod_1, _shared_rmod_2, _shared_rmod_3],
    system_module=_smod_enb_1,
)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.194", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_enb, _ru1_pdu_enb, _ru2_pdu_enb, _ru3_pdu_enb]
_tl_cloud_topology = "CLOUD_SRAN_L_ASIA_3xABIA_3xAHFIB_UTECA"

tl = TestLine(
    core=_realcore,
    enbs=[_enb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
