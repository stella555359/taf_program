# ##########################################################################################
#
#    7_20_UTE5GCLASSSV172  -  IV_PS_172  -  CV172
#
#    2024-01-08 11:06:41.702319:
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

# ------------------------ BTS CONFIGURATION ------------------------

_du1_pdu_gnb = FPFH(addr="10.0.117.55", login="admin", password="admin", port_numbers=[1])
_du2_pdu_gnb = FPFH(addr="10.0.117.55", login="admin", password="admin", port_numbers=[2])
_ru1_pdu_gnb = FPFH(addr="10.28.1.4", login="admin", password="admin", port_numbers=[6])
_ru2_pdu_gnb = FPFH(addr="10.28.1.11", login="admin", password="admin", port_numbers=[5])

_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[6], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="BL1923V0A8J"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[5], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M220620978"
)

_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2],
    serial_number="L1204104633",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="106",
    product_code="473096A.106",
    rus=[_rmod_gnb_2],
    serial_number="L1204507377",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[1],
    serial_number="DH214946345",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du2_pdu_gnb.pdu_ports[2],
    serial_number="DH201860916",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=22371, instance_id=2072)
_du_2 = DU(airscale=_smod_gnb_2, global_bts_id=23359, instance_id=2072)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.6", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.6", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.6", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:11:3002:3/112", vlan_id="3500"),
    x2c=NetworkAddress(v4="2a00:8a00:40ff:c000:2:11:3002:7/112", vlan_id="3500"),
    x2u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:11:3002:6/112", vlan_id="3500"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=22371, instance_id=2072)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=23359, instance_id=2072, master=_gnb_sbts_1)
_gnb_sbts_1.slave = _gnb_sbts_2
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.204", password="uteUTE!", port=22, username="ute"),
)
#_test_pc_gnb_2 = TestPc(
#    connections=[
#
#       NetworkAddress(v4="192.168.255.119"),
#
#        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
#    ],
#    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.146", password="uteUTE!", port=22, username="ute"),
#)

# --- TRS addition ---

switchdict_ptp_1 = {
        'TorSwitch_type':'TPS',
        'TorSwitch_addr':'10.5.117.101',
        'TorSwitch_login':'admin',
        'TorSwitch_passwd':'Admin@TPS24',
        'TorSwitch_port':'port7',
        }

switchdict_synce_1 = {
        'TorSwitch_type':'TPS',
        'TorSwitch_addr':'10.5.117.101',
        'TorSwitch_login':'admin',
        'TorSwitch_passwd':'Admin@TPS24',
        'TorSwitch_port':'1/3/C7',
        }

switchdict_ptp = {
        '5G':switchdict_ptp_1,
        '4G':switchdict_ptp_1
        }

switchdict_synce = {
        '5G':switchdict_synce_1,
        '4G':switchdict_synce_1
        }

# ------------------------TL_CONFIGURATION------------------------

_pdus = [_du1_pdu_gnb, _du2_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSA_2xASIB_ABIA_ABIO_AHFIB_AEQQ_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
#    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
#    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    test_pcs=[_test_pc_gnb_1,],
    tl_cloud_topology=_tl_cloud_topology,
)

tl.tl_ptp = switchdict_ptp
tl.tl_synce = switchdict_synce

