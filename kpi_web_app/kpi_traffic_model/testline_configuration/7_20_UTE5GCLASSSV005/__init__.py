# ##########################################################################################
#
#    7_20_UTE5GCLASSSV005  -  IV_PS_005  -  CV005
#
#    2024-07-02 11:40:30.456279:
#    __init__.py generator (version 2.0 of 02/12/2023).
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

_du1_pdu_gnb = FPFH(addr="10.0.117.206", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.28.4.229", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.28.5.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.28.4.229", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.28.5.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.28.5.192", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_gnb = FPFH(addr="10.28.5.210", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_6 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1], radio_type="FRPD", ru_hw_group="NR_RADIO", serial_number="EA201110153"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3], radio_type="FRGY", ru_hw_group="NR_RADIO", serial_number="K9165018737"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2], radio_type="FXDB", ru_hw_group="NR_RADIO", serial_number="F7162481330"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[2], radio_type="FRGY", ru_hw_group="NR_RADIO", serial_number="K9165018740"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[3], radio_type="FRGY", ru_hw_group="NR_RADIO", serial_number="K9165018736"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru6_pdu_gnb.pdu_ports[6], radio_type="FRMF", ru_hw_group="NR_RADIO", serial_number="L1170804106"
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[],
    hardware_type="ASOG",
    hardware_version="476254A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[5],
    serial_number="EA221253265",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=900140, instance_id=900128)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.150.145/0"), v4="10.14.48.13", vlan_id="1450"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.13", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.13", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.14.150.189/30", vlan_id="1281"),
    x2c=NetworkAddress(v4="10.14.150.189/30", vlan_id="1281"),
    x2u=NetworkAddress(v4="10.14.150.189/30", vlan_id="1281"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=900140, instance_id=900128)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.217", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb, _ru4_pdu_gnb, _ru5_pdu_gnb, _ru6_pdu_gnb]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSA_ASOG__3xAHPMDB_3xAHEGG_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
