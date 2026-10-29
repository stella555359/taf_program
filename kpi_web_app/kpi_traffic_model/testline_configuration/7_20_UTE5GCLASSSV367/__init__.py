# ##########################################################################################
#
#    7_20_UTE5GCLASSSV367  -  IV_PS_367  -  CV367
#
#    2023-12-04 21:50:41
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

# ##############################################################################
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ##############################################################################

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="10.0.117.112", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.28.1.86", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.174", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.173", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.28.1.85", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.28.1.87", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_gnb_8 = RU(
   # ok verifie correspond a RMOD-8 AEHC AH231800614 http://10.28.1.86/ output1
    pdu_port = _ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="AH231800614",
)
_rmod_gnb_6 = RU(
   # ok verifie correspond a RMOD-6 AHFIB BL2049V0V9J http://10.0.117.174/ output 2
    pdu_port = _ru2_pdu_gnb.pdu_ports[2],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="BL2049V0V9J",
)
_rmod_gnb_1 = RU(
    # ok verifie correspond a RMOD-1 AHLOA K9183926254 http://10.0.117.173/ output 1
    pdu_port = _ru3_pdu_gnb.pdu_ports[1],
    radio_type="AHLOA",
    ru_hw_group="NR_RADIO",
    serial_number="K9183926254",
)
_rmod_gnb_4 = RU(
    # ok verifie correspond a RMOD-4 AHFIB K9183827888  http://10.0.117.173/ output 2
    pdu_port = _ru3_pdu_gnb.pdu_ports[2],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="K9183827888",
)
_rmod_gnb_2 = RU(
    # ok verifie correspond a RMOD-2 AHLOA K9183926271  http://10.0.117.173/ output 4
    pdu_port = _ru3_pdu_gnb.pdu_ports[4],
    radio_type="AHLOA",
    ru_hw_group="NR_RADIO",
    serial_number="K9183926271",
)
_rmod_gnb_7 = RU(
    # ok verifie correspond a RMOD-7 AEHC AH231800606 http://10.28.1.85/ output 1
    pdu_port = _ru4_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="AH231800606",
)
_rmod_gnb_3 = RU(
    # ok verifie correspond a RMOD-3 AHLOA K9183926261 http://10.0.117.174/ output 1
    pdu_port = _ru2_pdu_gnb.pdu_ports[1],
    radio_type="AHLOA",
    ru_hw_group="NR_RADIO",
    serial_number="K9183926261",
)
_rmod_gnb_9 = RU(
    # ok verifie correspond a RMOD-9 AEHC AH231800629  http://10.28.1.87/ output 1
    pdu_port = _ru5_pdu_gnb.pdu_ports[1],
    radio_type="AEHC",
    ru_hw_group="NR_RADIO",
    serial_number="AH231800629",
)
_rmod_gnb_5 = RU(
    # ok verifie correspond a RMOD-5 AHFIB BL2049V0V9L http://10.0.117.173/ output 5
    pdu_port = _ru3_pdu_gnb.pdu_ports[5],
    radio_type="AHFIB",
    ru_hw_group="NR_RADIO",
    serial_number="BL2049V0V9L",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_7, _rmod_gnb_9, _rmod_gnb_8],
    serial_number="L1204104693",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_3, _rmod_gnb_6, _rmod_gnb_1, _rmod_gnb_5, _rmod_gnb_2, _rmod_gnb_4],
    serial_number="L1204105000",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIL",
    hardware_version="474767A.101",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[6],
    serial_number="DH220640311",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=1,
    instance_id=367,
    rus=[
        _rmod_gnb_8,
        _rmod_gnb_6,
        _rmod_gnb_1,
        _rmod_gnb_4,
        _rmod_gnb_2,
        _rmod_gnb_7,
        _rmod_gnb_3,
        _rmod_gnb_9,
        _rmod_gnb_5,
    ],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.28.25.46/30"), v4="10.14.49.34", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.34", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.34", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.25.42/29", vlan_id="4003"),
    x2c=NetworkAddress(v4="10.28.25.41/29", vlan_id="4003"),
    x2u=NetworkAddress(v4="10.28.25.41/29", vlan_id="4003"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=1, instance_id=367)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.95", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSA_ASIL_2xABIO_3xAHFIB_3xAEHC_3xAHLOA_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
