# ##########################################################################################
#
#    7_20_UTE5GCLASSSV382_1  -  IV_PS_2_1  -  CV2_1
#
#    2024-07-12 06:21:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "Nicolas Meillet"
__team__ = "MN RAN RD VRF NPS 1"
__email__ = "nicolas.meillet@nokia.com"

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

_du1_pdu_gnb = FPFH(addr="10.28.1.106", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.89", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.116.90", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.97.234", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru10_pdu_gnb = FPFH(addr="10.0.96.3", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[6],
    radio_type="AHEGC", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="EA211553651",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.122", port=5001),  
        ]
    )
)
_rmod_gnb_7 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5],
    radio_type="ARHA", 
    ru_hw_group="FRMr5.1_1_6T6R", 
    serial_number="1M211517615",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.128", port=5001),  
        ]
    )
)
_rmod_gnb_8 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[5],
    radio_type="ARHA", 
    ru_hw_group="FRMr5.1_1_6T6R", 
    serial_number="AS220308073",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.129", port=5001),  
        ]
    )
)
_rmod_gnb_9 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[5],
    radio_type="ARHA", 
    ru_hw_group="FRMr5.1_1_6T6R", 
    serial_number="1M211517581",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.130", port=5001),  
        ]
    )
)
_rmod_gnb_10 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[4],
    radio_type="AHPMDB", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="AS211416804",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.125", port=5001),  
        ]
    )
)
_rmod_gnb_11 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[5],
    radio_type="AHPMDB", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="AS211416819",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.126", port=5001),  
        ]
    )
)
_rmod_gnb_12 = RU(
    pdu_port=_ru10_pdu_gnb.pdu_ports[6],
    radio_type="AHPMDB", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="AS211416825",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.127", port=5001),  
        ]
    )
)
_rmod_gnb_14 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4],
    radio_type="AVQC", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M244409889",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.131", port=5001),  
        ]
    )
)
_rmod_gnb_15 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4],
    radio_type="AVQC", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M244409870",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.132", port=5001),  
        ]
    )
)
_rmod_gnb_16 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4],
    radio_type="AVQC", 
    ru_hw_group="cMAAr7.1_32T32R", 
    serial_number="1M244409878",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.133", port=5001),  
        ]
    )
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[6],
    radio_type="AHEGC", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="EA200150233",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.123", port=5001),  
        ]
    )
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[6],
    radio_type="AHEGC", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="EA211553652",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.124", port=5001),  
        ]
    )
)
_fsp_gnb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="102",
    product_code="475266A.102",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12],
    serial_number="L1211706194",
)
_fsp_gnb_5 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="102",
    product_code="475266A.102",
    rus=[_rmod_gnb_14, _rmod_gnb_15, _rmod_gnb_16],
    serial_number="L1211706210",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1173800892",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="102",
    product_code="473096A.102",
    rus=[],
    serial_number="L1162615759",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9, _rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12],
    serial_number="L1223806959",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[1],
    serial_number="DH201860727",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[_fsp_gnb_4, _fsp_gnb_5],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[2],
    serial_number="L1203608975",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_1 = DU(airscale=_smod_gnb_1, 
    global_bts_id=900006, 
    instance_id=900006,
     rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_10, _rmod_gnb_11, _rmod_gnb_12, _rmod_gnb_7, _rmod_gnb_9, _rmod_gnb_8, _rmod_gnb_16, _rmod_gnb_15, _rmod_gnb_14]
)
_du_2 = DU(airscale=_smod_gnb_2, 
    global_bts_id=900006, 
    instance_id=900006,
     rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_16, _rmod_gnb_15, _rmod_gnb_14]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(routing_v4=RoutingInformation(gateway="1172.20.8.158/32"), v4="10.14.147.97"),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.147.97", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.147.97", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.14.147.100/32"),
    x2c=NetworkAddress(v4="10.14.147.101/32"),
    x2u=NetworkAddress(v4="10.14.147.100/32"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=900006, instance_id=900006)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=900006, instance_id=900006, master=_gnb_sbts_1)
# _gnb_sbts_1.slave = _gnb_sbts_2
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.214", password="uteUTE!", port=22, username="ute"),
)
_test_pc_gnb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.219", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru10_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSASA_2xASIB_3xABIO_2xABIA_AEQQ_2xAHEGC_AZQJ_2xAHPMDB_2xARHA_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
