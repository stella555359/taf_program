# ##########################################################################################
#
#    7_20_UTE5GCLASSSV342  -  IV_PS_342  -  CV342
#
#    2026-01-20 10:22:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Rhizlane Benali"
__team__ = "MN RAN RD VRF NPS 1"
__email__ = "rhizlane.benali@nokia.com"

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

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_du1_pdu_gnb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.116.73", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.116.74", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5],
    radio_type="AHPMDG",
    ru_hw_group="FRMr6.2_4T4R",
    serial_number="LR253004995",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.141", port=5001),
        ]
    )
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[5],
    radio_type="AHPMDG",
    ru_hw_group="FRMr6.2_4T4R",
    serial_number="LR253004959",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.140", port=5001),
        ]
    )
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[5],
    radio_type="AHPMDG",
    ru_hw_group="FRMr6.2_4T4R",
    serial_number="LR253004961",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.139", port=5001),
        ]
    )
)
_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4],
    radio_type="AVQQ",
    ru_hw_group="cMAAr7.1_32T32R",
    serial_number="1M243305116",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.138", port=5001),
        ]
    )
)
_rmod_gnb_5 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4],
    radio_type="AVQQ",
    ru_hw_group="cMAAr7.1_32T32R",
    serial_number="1M243305117",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.137", port=5001),
        ]
    )
)
_rmod_gnb_6 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4],
    radio_type="AVQQ",
    ru_hw_group="cMAAr7.1_32T32R",
    serial_number="1M243305118",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.136", port=5001),
        ]
    )
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="104",
    product_code="473096A.104",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="EA194454147",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1223806956",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6],
    serial_number="L1223901435",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[1],
    serial_number="L1203002119",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1,
    global_bts_id=23287,
    instance_id=720342,
     rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_5, _rmod_gnb_6, _rmod_gnb_4]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.254/0"), v4="10.14.48.37", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.37", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.37", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.102.66/29", vlan_id="4004"),
    x2c=NetworkAddress(v4="10.0.102.65/29", vlan_id="4004"),
    x2u=NetworkAddress(v4="10.0.102.66/29", vlan_id="4004"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23287, instance_id=720342)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.152", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb]
_tl_cloud_topology = "CLOUD_SRAN_NLWG_NSASA_ASIB_ABIA_2xABIO_3xAVQQ_3xAHPMDG_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
