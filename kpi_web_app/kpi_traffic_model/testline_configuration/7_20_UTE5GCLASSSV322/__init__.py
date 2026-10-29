# ##########################################################################################
#
#    7_20_UTE5GCLASSSV322  -  IV_PS_322  -  CV322
#
#    2023-11-20 07:42:33.298021:
#    __init__.py generator (version 1.0 of 21/09/2023).
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
from taf.config.testline.radio import RU  
from taf.config.testline.lmi import SerialOverTcp, Remote


# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_du1_pdu_gnb = FPFH(addr="10.0.117.162", login="admin", password="admin", port_numbers=[1])
_ru1_pdu_gnb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[1])
_ru2_pdu_gnb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[3])
_ru3_pdu_gnb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[2])
_ru4_pdu_gnb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[1])
_ru5_pdu_gnb = FPFH(addr="10.0.117.188", login="admin", password="admin", port_numbers=[2])
_ru6_pdu_gnb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[2])
_ru7_pdu_gnb = FPFH(addr="10.0.117.188", login="admin", password="admin", port_numbers=[1])
_ru8_pdu_gnb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[3])
_rmod_gnb_6 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="cMAAr6.1_64T64R",
    serial_number="1M215219033",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.118", port=5001),  
        ]  
    )
)
_rmod_gnb_1 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[3],
    radio_type="ARDA",
    ru_hw_group="FRMr5.1_1_6T6R",
    serial_number="K9204232118",
)
_rmod_gnb_3 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[2],
    radio_type="AREA",
    ru_hw_group="FRMr5.1_1_6T6R",
    serial_number="EA203654824",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.115", port=5001),  
        ]  
    )
)
_rmod_gnb_8 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="cMAAr6.1_64T64R",
    serial_number="1M201311434",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.120", port=5001),  
        ]  
    )
)
_rmod_gnb_4 = RU(
    pdu_port = _ru5_pdu_gnb.pdu_ports[2],
    radio_type="ARGA",
    ru_hw_group="FRMr5.1_1_6T6R",
    serial_number="AS204611936",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.116", port=5001),  
        ]  
    )
)
_rmod_gnb_2 = RU(
    pdu_port = _ru6_pdu_gnb.pdu_ports[2],
    radio_type="ARHA",
    ru_hw_group="FRMr5.1_1_6T6R",
    serial_number="1M211517652",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.114", port=5001),  
        ]  
    )
)
_rmod_gnb_7 = RU(
    pdu_port = _ru7_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="cMAAr6.1_64T64R",
    serial_number="1M201304438",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.119", port=5001),  
        ]  
    )
)
_rmod_gnb_5 = RU(
    pdu_port = _ru8_pdu_gnb.pdu_ports[3],
    radio_type="ARPA",
    ru_hw_group="FRMr5.1_1_6T6R",
    serial_number="F7201011427",
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.14.152.117", port=5001),  
        ]  
    )
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="104",
    product_code="473096A.104",
    rus=[_rmod_gnb_1],
    serial_number="L1200100597",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_4, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_5],
    serial_number="L1204108998",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="104",
    product_code="475266A.104",
    rus=[_rmod_gnb_6, _rmod_gnb_7, _rmod_gnb_8],
    serial_number="L1213108383",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_3, _fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[1],
    serial_number="L1192905062",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=23135,
    instance_id=720322,
    rus=[_rmod_gnb_6, _rmod_gnb_1, _rmod_gnb_3, _rmod_gnb_8, _rmod_gnb_4, _rmod_gnb_2, _rmod_gnb_7, _rmod_gnb_5],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.232", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.232", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.232", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.11.106/29", vlan_id="4001"),
    x2c=NetworkAddress(v4="10.28.11.105/29", vlan_id="4001"),
    x2u=NetworkAddress(v4="10.28.11.106/29", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23135, instance_id=720322)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.72", password="uteUTE!", port=22, username="ute"),
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
]

_tl_cloud_topology = "CLOUD_SRAN_NLWG_NSA_ASIB_ABIA_2xABIO_3xAEQE_ARHA_ARGA_ARDA_ARPA_AREA_UTECA"

tl = TestLine(
    core=_realcore,
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
