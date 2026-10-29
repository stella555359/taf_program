# ##########################################################################################
#
#    7_20_UTE5GCLASSSV323  -  IV_PS_323  -  CV323
#
#    2023-11-20 13:39:18.350148:
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = "AMINA LAKHDARI"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "amina.lakhdari@nokia.com"

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

_du1_pdu_gnb = FPFH(addr="10.0.117.162", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.198", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.199", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.200", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru10_pdu_gnb = FPFH(addr="10.0.117.201", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru12_pdu_gnb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_10 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[2],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242706884",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.80", port=5001),  
        ]
    )
)
_rmod_gnb_11 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[3],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242702500",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.81", port=5001),  
        ]
    )
)
_rmod_gnb_12 = RU(
    pdu_port=_ru12_pdu_gnb.pdu_ports[3],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242706978",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.82", port=5001),  
        ]
    )
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AVQD", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M252208384"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1],
    radio_type="AVQD", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M243403466"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1],
    radio_type="AVQD", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M252208383"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="BL2310H601R",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.83", port=5001),  
        ]
    )
)
_rmod_gnb_5 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="BL2314H605J",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.84", port=5001),  
        ]
    )
)
_rmod_gnb_6 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="BL2312H604Z",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.85", port=5001),  
        ]
    )
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6, _rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12],
    serial_number="L1204108999",
)

_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12],
    serial_number="L1173619579",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[3],
    serial_number="L1192401133",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, 
    global_bts_id=23133, 
    instance_id=720323,
     rus=[_rmod_gnb_1, _rmod_gnb_3, _rmod_gnb_2, _rmod_gnb_4, _rmod_gnb_6, _rmod_gnb_5]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.49.91", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.91", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.91", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.6.250/29", vlan_id="4002"),
    x2c=NetworkAddress(v4="10.28.6.250/29", vlan_id="4002"),
    x2u=NetworkAddress(v4="10.28.6.250/29", vlan_id="4002"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23133, instance_id=720323)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.43", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru10_pdu_gnb,
    _ru12_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_SRAN_NLW_NSASA_ASIB_ABIA_2xABIO_3xAHEGB_2xAVQE_3xAHPMDB_3xAHHB_UTECA"

tl = TestLine(
    core=_realcore,
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
