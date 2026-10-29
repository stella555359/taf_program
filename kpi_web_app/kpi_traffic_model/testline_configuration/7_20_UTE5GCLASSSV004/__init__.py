#   ##########################################################################################
#
#    7_20_UTE5GCLASSSV004  -  IV_PS_004  -  CV004
#
#    Update: 2026-03-12 : Edrice Hachemi
#    
#
# ##########################################################################################

__maintainer__ = "Edrice Hachemi"
__team__ = "MN RAN RD VRF NPS 1"
__email__ = "edrice.hachemi@nokia.com"

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

_du1_pdu_gnb = FPFH(addr="10.0.117.163", login="admin", password="admin", port_numbers=[5])
_ru1_pdu_gnb = FPFH(addr="10.0.116.88", login="admin", password="admin", port_numbers=[4])
_ru2_pdu_gnb = FPFH(addr="10.0.116.87", login="admin", password="admin", port_numbers=[4])
_ru3_pdu_gnb = FPFH(addr="10.0.116.86", login="admin", password="admin", port_numbers=[4])
_ru4_pdu_gnb = FPFH(addr="10.0.116.86", login="admin", password="admin", port_numbers=[6])
_ru5_pdu_gnb = FPFH(addr="10.0.116.88", login="admin", password="admin", port_numbers=[6])
_ru6_pdu_gnb = FPFH(addr="10.0.116.87", login="admin", password="admin", port_numbers=[6])
_ru7_pdu_gnb = FPFH(addr="10.0.116.85", login="admin", password="admin", port_numbers=[5])
_ru8_pdu_gnb = FPFH(addr="10.0.116.85", login="admin", password="admin", port_numbers=[6])
_ru9_pdu_gnb = FPFH(addr="10.0.116.85", login="admin", password="admin", port_numbers=[4])
_ru10_pdu_gnb = FPFH(addr="10.0.116.88", login="admin", password="admin", port_numbers=[5])
_ru11_pdu_gnb = FPFH(addr="10.0.116.87", login="admin", password="admin", port_numbers=[5])
_ru12_pdu_gnb = FPFH(addr="10.0.116.86", login="admin", password="admin", port_numbers=[5])
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M203136585"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M210537349"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M222414828"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA193170793"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="L1182400459"
)
_rmod_gnb_6 = RU(
    pdu_port=_ru6_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="L1182401424"
)
_rmod_gnb_7 = RU(
    pdu_port=_ru7_pdu_gnb.pdu_ports[5], radio_type="AHEGC", ru_hw_group="NR_RADIO", serial_number="EA200150237"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru8_pdu_gnb.pdu_ports[6], radio_type="AHEGC", ru_hw_group="NR_RADIO", serial_number="EA211553648"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru9_pdu_gnb.pdu_ports[4], radio_type="AHEGC", ru_hw_group="NR_RADIO", serial_number="EA222551294"
)
_rmod_gnb_10 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[5], radio_type="AHPMDB", ru_hw_group="NR_RADIO", serial_number="LR230705946"
)
_rmod_gnb_11 = RU(
    pdu_port=_ru11_pdu_gnb.pdu_ports[5], radio_type="AHPMDB", ru_hw_group="NR_RADIO", serial_number="LR243606492"
)
_rmod_gnb_12 = RU(
    pdu_port=_ru12_pdu_gnb.pdu_ports[5], radio_type="AHPMDB", ru_hw_group="NR_RADIO", serial_number="AS205204318"
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1204008428",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6, _rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9],
    serial_number="L1223901371",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12],
    serial_number="RW191801839",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[5],
    serial_number="L1200900060",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=720004, instance_id=720004)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.254/0"), v4="10.14.48.38", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.38", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.38", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.16.180/32", vlan_id="4032"),
    x2c=NetworkAddress(v4="10.0.102.153/29", vlan_id="4006"),
    x2u=NetworkAddress(v4="10.28.16.180/32", vlan_id="4032"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=720004, instance_id=720004)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.213", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb, _ru4_pdu_gnb]
_tl_cloud_topology = "CLOUD_SRAN_NL_SA_NSA_ASIB_ABIO_ABIO_ABIA_AEQQ_AHHB_AHEGC_AHPMDB_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
