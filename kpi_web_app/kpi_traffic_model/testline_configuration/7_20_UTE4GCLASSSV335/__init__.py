# ##########################################################################################
#
#    7_20_UTE4GCLASSSV335  -  IV_PS_335  -  CV335
#
#    2023-12-05 19:28:32.838764:
#    __init__.py generator (version 2.0 of 02/12/2023).
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

_du1_pdu_enb = FPFH(addr="10.0.117.96", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.117.188", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.189", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_enb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_enb = FPFH(addr="10.0.117.190", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_enb = FPFH(addr="10.0.117.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_shared_rmod_14 = RU(
    pdu_port = _ru1_pdu_enb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182107374",
)
_rmod_enb_10 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182614353",
)
_rmod_enb_11 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914830",
)
_rmod_enb_15 = RU(
    pdu_port = _ru4_pdu_enb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182614354",
)
_shared_rmod_2 = RU(
    pdu_port = _ru1_pdu_enb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWMG",
)
_rmod_enb_12 = RU(
    pdu_port = _ru5_pdu_enb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914827",
)
_shared_rmod_3 = RU(
    pdu_port = _ru4_pdu_enb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWML",
)
_shared_rmod_1 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWLU",
)
_rmod_enb_13 = RU(
    pdu_port = _ru6_pdu_enb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914829",
)
_shared_rmod_8 = RU(
    pdu_port = _ru5_pdu_enb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGXT",
)
_shared_rmod_9 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGUN",
)
_shared_rmod_7 = RU(
    pdu_port = _ru6_pdu_enb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGWY",
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_9, _shared_rmod_7, _shared_rmod_8],
    serial_number="EA192178938",
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_15, _shared_rmod_14, _rmod_enb_10],
    serial_number="EA192178885",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_13, _shared_rmod_14, _rmod_enb_12, _shared_rmod_2, _rmod_enb_11, _shared_rmod_3],
    serial_number="EA192178820",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_3, _fsp_enb_2, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.204",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[4],
    serial_number="L1201109779",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22331,
    instance_id=22331,
    oam_ip=NetworkAddress(v4="10.14.48.119"),
    rms=[
        _rmod_enb_13,
        _shared_rmod_1,
        _rmod_enb_12,
        _shared_rmod_2,
        _rmod_enb_11,
        _shared_rmod_3,
        _rmod_enb_15,
        _shared_rmod_7,
        _rmod_enb_10,
        _shared_rmod_9,
        _shared_rmod_14,
        _shared_rmod_8,
    ],
    system_module=_smod_enb_1,
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.121", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_enb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
    _ru4_pdu_enb,
    _ru5_pdu_enb,
    _ru6_pdu_enb,
]
_tl_cloud_topology = "CLOUD_SRAN_L_ASIA_3xABIA_3xAHNA_3xUHFA_3xAHLBA_3xUHIE_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
