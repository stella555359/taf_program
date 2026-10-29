# ##########################################################################################
#
#    7_20_UTE4GCLASSSV343_1  -  IV_PS_3_1  -  CV3_1
#
#    2024-06-20 12:17:28.684118:
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

_du1_pdu_enb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_du2_pdu_enb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.116.254", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.116.255", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_enb_4 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381647"
)
_rmod_enb_5 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381642"
)
_rmod_enb_1 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[4], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="EA222752596"
)
_rmod_enb_3 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[6], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9182709936"
)
_rmod_enb_9 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9181925280"
)
_rmod_enb_6 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381645"
)
_rmod_enb_2 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[5], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9181625747"
)
_rmod_enb_8 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9193933072"
)
_rmod_enb_7 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9181925259"
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2],
    serial_number="L1172902335",
)
_fsp_enb_5 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="EA192178830"
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_6, _rmod_enb_4, _rmod_enb_5],
    serial_number="L1173607987",
)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="K9172529981"
)
_fsp_enb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_9, _rmod_enb_7, _rmod_enb_8],
    serial_number="EA192178866",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_2, _fsp_enb_3, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[4],
    serial_number="L1212115869",
)
_fct_enb_2 = CommonUnit(
    capacity_units=[_fsp_enb_5, _fsp_enb_4],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du2_pdu_enb.pdu_ports[3],
    serial_number="L1173422528",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_smod_enb_2 = Airscale(common_units=[_fct_enb_2])
_enb_sbts_1 = RealEnb(
    global_bts_id=23322,
    instance_id=343,
    oam_ip=NetworkAddress(v4="10.14.48.68"),
    rms=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2, _rmod_enb_6, _rmod_enb_4, _rmod_enb_5],
    system_module=_smod_enb_1,
)
_enb_sbts_2 = RealEnb(master=_enb_sbts_1, rms=[_rmod_enb_9, _rmod_enb_7, _rmod_enb_8], system_module=_smod_enb_2)
_enb_sbts_1.slave = _enb_sbts_2
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.118", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.119"),
        Connection(device=_enb_sbts_2.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.189", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_enb,
    _du2_pdu_enb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
    _ru4_pdu_enb,
]
#_tl_cloud_topology = "CLOUD_SRAN_LWG_2xASIA_5xABIA_3xAHHB_3xAHPMDA_3xAHEGB_UTECA"
_tl_cloud_topology = "CLOUD_SRAN_L_ASIAA_3xABIA_3xUHFA_3xAHCA_3xUHIE_3xUHBA_UTECA"


tl = TestLine(
    enbs=[_enb_sbts_1, _enb_sbts_2],
    pdus=_pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_enb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
