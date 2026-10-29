# ##########################################################################################
#
#    7_20_UTE5GCLASSSV114  -  IV_PS_114  -  CV114
#
#    Update date: 09-02-2026
#    __init__.py 
#
# ##########################################################################################

__maintainer__ = "Abderrahmane NEZROUk"
__team__ = "MI MN RAN RD VRF NPS 2"
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
from taf.config.testline.nms import NMS, NetAct
from taf.config.testline.gnb.du import Cablink, Endpoint

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="1.1.1.1", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="1.1.1.1", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1], radio_type="AHFIC", ru_hw_group="NR_RADIO", serial_number="K9183616287"
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="102",
    product_code="475792A.102",
    rus=[_rmod_gnb_1],
    serial_number="L1242407189",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIM",
    hardware_version="475765A.104",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[1],
    serial_number="L1234206447",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23182, instance_id=23182)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.254/0"), v4="10.14.49.132", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.132", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.132", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.15.9/29", vlan_id="4001"),
    x2c=NetworkAddress(v4="10.28.15.10/29", vlan_id="4001"),
    x2u=NetworkAddress(v4="10.28.15.9/29", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23182, instance_id=23182)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.185", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIM_ABIP_AHFIC_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
