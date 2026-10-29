# ##########################################################################################
#
#    7_20_UTE5GCLASSSV394  -  IV_PS_394  -  CV394
#
#    2024-08-27 15:42:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################
__maintainer__ = "A NEZROUK"
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
from taf.config.testline.flexi import Flexi
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
_du1_pdu_gnb = FPFH(addr="10.0.117.153", login="admin", password="admin", port_numbers=[6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.54", login="admin", password="admin", port_numbers=[4])
_ru2_pdu_gnb = FPFH(addr="10.0.116.115", login="admin", password="admin", port_numbers=[4])
_ru3_pdu_gnb = FPFH(addr="10.0.117.209", login="admin", password="admin", port_numbers=[4])
_ru4_pdu_gnb = FPFH(addr="10.0.116.54", login="admin", password="admin", port_numbers=[6])
_ru5_pdu_gnb = FPFH(addr="10.0.116.115", login="admin", password="admin", port_numbers=[6])
_ru6_pdu_gnb = FPFH(addr="10.0.117.209", login="admin", password="admin", port_numbers=[6])
_ru7_pdu_gnb = FPFH(addr="10.0.116.212", login="admin", password="admin", port_numbers=[4])
_ru8_pdu_gnb = FPFH(addr="10.0.116.212", login="admin", password="admin", port_numbers=[5])
_ru9_pdu_gnb = FPFH(addr="10.0.116.212", login="admin", password="admin", port_numbers=[6])
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4], radio_type="AVQQ", ru_hw_group="NR_RADIO", serial_number="1M241603401"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4], radio_type="AVQQ", ru_hw_group="NR_RADIO", serial_number="1M240403973"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4], radio_type="AVQQ", ru_hw_group="NR_RADIO", serial_number="1M242100043"
)
_rmod_gnb_7 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[6], radio_type="AHPMDG", ru_hw_group="NR_RADIO", serial_number="BL2409C6HLO"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[6], radio_type="AHPMDG", ru_hw_group="NR_RADIO", serial_number="BL2409C6HGQ"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru6_pdu_gnb.pdu_ports[6], radio_type="AHPMDG", ru_hw_group="NR_RADIO", serial_number="BL2409C6HLC"
)
_rmod_gnb_22 = RU(
    pdu_port=_ru7_pdu_gnb.pdu_ports[4], radio_type="AHEGHA", ru_hw_group="NR_RADIO", serial_number="K9243932697"
)
_rmod_gnb_23 = RU(
    pdu_port=_ru8_pdu_gnb.pdu_ports[5], radio_type="AHEGHA", ru_hw_group="NR_RADIO", serial_number="K9243932693"
)
_rmod_gnb_24 = RU(
    pdu_port=_ru9_pdu_gnb.pdu_ports[6], radio_type="AHEGHA", ru_hw_group="NR_RADIO", serial_number="K9243932698"
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIQ",
    hardware_version="101",
    product_code="476397A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1232305682",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9, _rmod_gnb_22, _rmod_gnb_23, _rmod_gnb_24],
    serial_number="L1223901456",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="106",
    product_code="473096A.106",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9],
    serial_number="L1204507336",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="DH250409866",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23288, instance_id=720394)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="1None"), v4="10.14.48.181", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.181", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.181", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.102.202/29", vlan_id="4006"),
    x2c=NetworkAddress(v4="10.0.102.201/29", vlan_id="4006"),
    x2u=NetworkAddress(v4="10.0.102.202/29", vlan_id="4006"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23288, instance_id=720394)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.155", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
    _ru6_pdu_gnb,
    _ru7_pdu_gnb,
    _ru8_pdu_gnb,
    _ru9_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSASA_ASIM_ABIQ_ABIO_ABIA_3xAVQQ_3xAHPMDG_3xAHEGHA_UTECA"
tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)