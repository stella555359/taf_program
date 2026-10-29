# ##########################################################################################
#
#    7_20_UTE5GCLASSSV392_1  -  IV_PS_2_1  -  CV2_1
#
#    2024-07-12 06:16:
#    __init__.py generator (version 2.4 of 03/07/2024).
#    Updated by Marie Boutillier - 22/12/2025.
# ##########################################################################################

__maintainer__ = "Marie Boutillier"
__team__ = "MN RAN RD VRF NPS 1 (L05)"
__email__ = "marie.boutillier@nokia.com"

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
from taf.config.testline.lmi import SerialOverTcp, Remote

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="10.28.1.106", login="admin", password="admin", port_numbers=[3])
_du2_pdu_gnb = FPFH(addr="10.28.1.106", login="admin", password="admin", port_numbers=[4])
_ru1_pdu_gnb = FPFH(addr="10.0.117.213", login="admin", password="admin", port_numbers=[5])
_ru5_pdu_gnb = FPFH(addr="10.0.117.213", login="admin", password="admin", port_numbers=[4])
_rmod_gnb_5 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[4],
    radio_type="ARGA", 
    ru_hw_group="FRMr5.1_1_6T6R", 
    serial_number="F7204202749",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.93", port=5001),  
        ]
    )
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5], 
    radio_type="AREA", 
    ru_hw_group="FRMr5.1_1_6T6R", 
    serial_number="EA203654847",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.92", port=5001),  
        ]
    )
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_1],
    serial_number="L1183411386",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_5],
    serial_number="L1183511771",
)
_fsp_gnb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_5],
    serial_number="L1204104612",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[3],
    serial_number="L1214315552",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[_fsp_gnb_4],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du2_pdu_gnb.pdu_ports[4],
    serial_number="L1214315518",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_1 = DU(airscale=_smod_gnb_1, 
    global_bts_id=900162, 
    instance_id=900162,
     rus=[_rmod_gnb_1, _rmod_gnb_5]
)
_du_2 = DU(airscale=_smod_gnb_2, 
    global_bts_id=900162, 
    instance_id=900162,
    rus=[_rmod_gnb_1, _rmod_gnb_5]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(routing_v4=RoutingInformation(gateway="10.14.49.252/23"), v4="10.14.48.186"),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.186", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.186", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.14.147.60/32"),
    x2c=NetworkAddress(v4="10.14.147.61/32"),
    x2u=NetworkAddress(v4="10.14.147.60/32"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=900162, instance_id=900162)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=900162, instance_id=900162, master=_gnb_sbts_1)
# _gnb_sbts_1.slave = _gnb_sbts_2
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.215", password="uteUTE!", port=22, username="ute"),
)
_test_pc_gnb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.220", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _du2_pdu_gnb, _ru1_pdu_gnb, _ru5_pdu_gnb]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSASA_2xASIB_3xABIO_2xABIA_2xAQQQ_AZQJ_AHEGC_ARHA_AHPMDB_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
