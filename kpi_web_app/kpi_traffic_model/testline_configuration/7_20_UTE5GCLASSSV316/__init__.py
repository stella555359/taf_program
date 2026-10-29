# ##########################################################################################
#
#    7_20_UTE5GCLASSSV316  -  IV_PS_316  -  CV316
#
#    2025-06-23 11:02:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Thierry Leclercq"
__team__ = "MN RAN RD VRF NPS 1"
__email__ = "thierry.leclercq@nokia.com"

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
from taf.config.testline.lmi import SerialOverTcp, Remote

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(addr="10.0.117.96", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.189", login="admin", password="adminFPFH", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.190", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.191", login="admin", password="adminFPFH", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242633411",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.86", port=5001),  
        ]
    )
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242638569",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.87", port=5001),  
        ]
    )
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1],
    radio_type="AHPMDG", 
    ru_hw_group="FRMr6.2_4T4R", 
    serial_number="K9242638706",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.88", port=5001),  
        ]
    )
)
_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="K9243919293",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.89", port=5001),  
        ]
    )
)
_rmod_gnb_5 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="BL2314H605I",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.90", port=5001),  
        ]
    )
)
_rmod_gnb_6 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2],
    radio_type="AHEGHA", 
    ru_hw_group="FRMr6.2a_4T4R", 
    serial_number="BL2314H605D",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.91", port=5001),  
        ]
    )
)
_rmod_gnb_7 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[3],
    radio_type="AVQE", 
    ru_hw_group="cMAAr7.1_64T64R", 
    serial_number="L1233212895"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3],
    radio_type="AVQE", 
    ru_hw_group="cMAAr7.1_64T64R", 
    serial_number="L1233212899"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3],
    radio_type="AVQE", 
    ru_hw_group="cMAAr7.1_64T64R", 
    serial_number="L1233212896"
)

_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="EA192071761",
)
_fsp_gnb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1204008438",
)
_fsp_gnb_5 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="102",
    product_code="475792A.102",
    rus=[_rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6],
    serial_number="L1241104184",
)
_fsp_gnb_6 = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="102",
    product_code="475792A.102",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9],
    serial_number="L1242304447",
)

_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[5],
    serial_number="L1201106466",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[_fsp_gnb_4, _fsp_gnb_5, _fsp_gnb_6],
    hardware_type="ASIM",
    hardware_version="104",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="L1242410081",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_2 = DU(airscale=_smod_gnb_2, 
    global_bts_id=23221, 
    instance_id=720316,
     rus=[_rmod_gnb_4, _rmod_gnb_6, _rmod_gnb_5, _rmod_gnb_7, _rmod_gnb_9, _rmod_gnb_8, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_1]
)
_du_1 = DU(airscale=_smod_gnb_1, 
    global_bts_id=23221, 
    instance_id=720316,
     rus=[_rmod_gnb_4, _rmod_gnb_6, _rmod_gnb_5, _rmod_gnb_7, _rmod_gnb_9, _rmod_gnb_8,_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.252/23"), v4="10.14.48.157", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.157", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.157", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.16.27/32"),
    x2c=NetworkAddress(v4="10.28.16.27/32"),
    x2u=NetworkAddress(v4="10.28.16.27/32"),
)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=23221, instance_id=720316)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23221, instance_id=720316, master=_gnb_sbts_2)
_gnb_sbts_2.slave = _gnb_sbts_1
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.122", password="uteUTE!", port=22, username="ute"),
)
_test_pc_gnb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.158", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb
]
_tl_cloud_topology = "CLOUD_SRAN_NLWG_NSASA_2xASIB_ABIA_3xABIO_3xAHPMDG_AVQQ_3xAHEGHA_2xAVQE_UTECA"

tl = TestLine(
    core=_realcore,
    gnbs=[_gnb_sbts_2, _gnb_sbts_1],
    ### pdus=_pdus,
    test_pc=_test_pc_gnb_2,
    test_pcs=[_test_pc_gnb_2, _test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
