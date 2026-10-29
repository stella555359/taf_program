# ##########################################################################################
#
#    7_20_UTE4GCLASSSV344  -  IV_PS_344  -  CV344
#
#    2023-11-20 08:01:22.004977:
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = ""
__team__ = "MN RAN Pz NPS SG1"
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
from taf.config.testline.lmi import SerialOverTcp, Remote

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_ru1_pdu_gnb = FPFH(addr="10.0.117.192", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.193", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.194", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])


_du1_pdu_enb = FPFH(addr="10.0.117.162", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.117.195", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.117.196", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.197", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_enb_1 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[3],
    radio_type="AHEGB", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="K9193933079",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.52", port=5001),  
        ]
    )
)
_rmod_enb_2 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[3],
    radio_type="AHEGB", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="K9193933078",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.53", port=5001),  
        ]
    )
)
_rmod_enb_3 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[3],
    radio_type="AHEGB", 
    ru_hw_group="FRMr5.1a_4T4R", 
    serial_number="EA204550299",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.54", port=5001),  
        ]
    )
)
_shared_rmod_4 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922513",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.49", port=5001),  
        ]
    )
)
_shared_rmod_5 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922515",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.50", port=5001),  
        ]
    )
)
_shared_rmod_6 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922534",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.51", port=5001),  
        ]
    )
)
_rmod_enb_7 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[3],
    radio_type="AHHB", 
    ru_hw_group="FRMr5.1_1_4T4R", 
    serial_number="EA205250593",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.55", port=5001),  
        ]
    )
)
_rmod_enb_8 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3],
    radio_type="AHHB", 
    ru_hw_group="FRMr5.1_1_4T4R", 
    serial_number="EA205250591",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.56", port=5001),  
        ]
    )
)
_rmod_enb_9 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3],
    radio_type="AHHB", 
    ru_hw_group="FRMr5.1_1_4T4R", 
    serial_number="EA205250567",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.57", port=5001),  
        ]
    )
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_1, _rmod_enb_2, _rmod_enb_3],
    serial_number="L1173606472",
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_4, _shared_rmod_5, _shared_rmod_6, _rmod_enb_7, _rmod_enb_8, _rmod_enb_9],
    serial_number="L1190106020",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1, _fsp_enb_3],
    hardware_type="ASIA",
    hardware_version="203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[5],
    serial_number="L1173502437",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22123,
    instance_id=344,
    oam_ip=NetworkAddress(v4="10.14.49.81"),
    rms=[
        _rmod_enb_1, 
        _shared_rmod_5, 
        _rmod_enb_8, 
        _rmod_enb_7, 
        _shared_rmod_6, 
        _shared_rmod_4, 
        _rmod_enb_2, 
        _rmod_enb_3, 
        _rmod_enb_9
    ],
    system_module=_smod_enb_1,
)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.188", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_enb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
]
_tl_cloud_topology = "CLOUD_SRAN_LW_ASIA_2xABIA_3xAHEGB_3xAHHB_3xAHPMDA_UTECA"

tl = TestLine(
    core=_realcore,
    enbs=[_enb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_enb_1,
    test_pcs=[_test_pc_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
