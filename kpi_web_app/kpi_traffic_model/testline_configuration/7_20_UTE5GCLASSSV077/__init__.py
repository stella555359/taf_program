# ##########################################################################################
#
#    iv_ps077  -  IV_PS_077  -  CV077
#
#    2025-08-22
#    
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUk"
__team__ = "MN RAN RD VRF NPS 2"
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

_du1_pdu_gnb = FPFH(addr="10.0.96.89", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.139", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.140", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.139", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.0.117.141", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.0.117.140", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[5], radio_type="AVQA", ru_hw_group="NR_RADIO", serial_number="L1251400633"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5], radio_type="AVQA", ru_hw_group="NR_RADIO", serial_number="L1251401787"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[6], radio_type="AHPB", ru_hw_group="NR_RADIO", serial_number="NQ242611799"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[5], radio_type="AVQA", ru_hw_group="NR_RADIO", serial_number="L1251401786"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[6], radio_type="AHPJ", ru_hw_group="NR_RADIO", serial_number="K9232737242"
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[],
    hardware_type="ASOE",
    hardware_version="475587A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[1],
    serial_number="EA213353929",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23181, instance_id=23181)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="1None"), v4="10.14.48.46", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.46", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.46", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.11.10/29", vlan_id="4004"),
    x2c=NetworkAddress(v4="10.28.11.9/29", vlan_id="4004"),
    x2u=NetworkAddress(v4="None"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23181, instance_id=23181)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.33", password="uteUTE!", port=22, username="ute"
    ),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb, _ru4_pdu_gnb, _ru5_pdu_gnb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASOE_AHPB_3xAVQA_AHPJ_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
