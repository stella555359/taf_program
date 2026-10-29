# ##########################################################################################
#
#    7_20_UTE4GCLASSSV324  -  IV_PS_324  -  CV324
#
#    2023-09-27 13:26:21.980072:
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUK"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "abderrahmane.nezrouk@nokia.com"

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

_du1_pdu = FPFH(addr="10.0.117.152", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu = FPFH(addr="10.0.116.54", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu = FPFH(addr="10.0.117.209", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu = FPFH(addr="10.0.116.212", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu = FPFH(addr="10.0.116.115", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_shared_rmod_1 = RU(
    pdu_port = _ru1_pdu.pdu_ports[2],
    radio_type="AHPMDD",
    ru_hw_group="AHPMDD_ru_hw_group",
    serial_number="6Q204500341",
)
_shared_rmod_2 = RU(
    pdu_port = _ru2_pdu.pdu_ports[2],
    radio_type="AHEGC",
    ru_hw_group="AHEGC_ru_hw_group",
    serial_number="EA222551294",
)
_shared_rmod_3 = RU(
    pdu_port = _ru1_pdu.pdu_ports[1],
    radio_type="AHPMDD",
    ru_hw_group="AHPMDD_ru_hw_group",
    serial_number="6Q204500338",
)
_shared_rmod_4 = RU(
    pdu_port = _ru1_pdu.pdu_ports[3],
    radio_type="AHPMDD",
    ru_hw_group="AHPMDD_ru_hw_group",
    serial_number="AS220600538",
)
_rmod_enb_5 = RU(
    pdu_port = _ru2_pdu.pdu_ports[3],
    radio_type="AHHB",
    ru_hw_group="AHHB_ru_hw_group",
    serial_number="DH221646120",
)
_shared_rmod_6 = RU(
    pdu_port = _ru3_pdu.pdu_ports[2],
    radio_type="AHEGC",
    ru_hw_group="AHEGC_ru_hw_group",
    serial_number="EA203950526",
)
_rmod_enb_7 = RU(
    pdu_port = _ru3_pdu.pdu_ports[3],
    radio_type="AHHB",
    ru_hw_group="AHHB_ru_hw_group",
    serial_number="DH221645995",
)
_shared_rmod_8 = RU(
    pdu_port = _ru4_pdu.pdu_ports[2],
    radio_type="AHEGC",
    ru_hw_group="AHEGC_ru_hw_group",
    serial_number="EA222551310",
)
_rmod_enb_9 = RU(
    pdu_port = _ru4_pdu.pdu_ports[3],
    radio_type="AHHB",
    ru_hw_group="AHHB_ru_hw_group",
    serial_number="DH221646156",
)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="104", product_code="473096A", serial_number="L1192400275"
)
_fsp_enb_2 = CapacityUnit(
    addr="", hardware_type="ABIO", hardware_version="104", product_code="475266A", serial_number="L1221702689"
)
_fsp_enb_3 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="104", product_code="473096A", serial_number="L1192400296"
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1, _fsp_enb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu.pdu_ports[1],
    serial_number="L1203611946",
)
_fct_enb_2 = CommonUnit(
    capacity_units=[_fsp_enb_2],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu.pdu_ports[2],
    serial_number="L1203700087",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_smod_enb_2 = Airscale(common_units=[_fct_enb_2])
_enb_sbts_1 = RealEnb(
    global_bts_id=22376,
    instance_id=324,
    oam_ip=NetworkAddress(v4="10.14.48.132"),
    rms=[_shared_rmod_1, _shared_rmod_3, _shared_rmod_4],
    system_module=_smod_enb_1,
)
_enb_sbts_2 = RealEnb(
    master=_enb_sbts_1,
    rms=[_shared_rmod_2, _rmod_enb_5, _shared_rmod_6, _rmod_enb_7, _shared_rmod_8, _rmod_enb_9],
    system_module=_smod_enb_2,
)
_enb_sbts_1.slave = _enb_sbts_2
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.207", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_2.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.210", password="uteUTE!", port=22, username="ute"),
)
_tl_cloud_topology = "CLOUD_SRAN_LWG_2xASIB_2xABIA_ABIO_3xAHPMDD_3xAHHB_3xAHEGC_ENB22376_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1, _enb_sbts_2],
    pdus = [_du1_pdu, _ru1_pdu, _ru2_pdu, _ru3_pdu, _ru4_pdu],
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_enb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
