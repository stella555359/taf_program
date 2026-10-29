# ##########################################################################################
#
#    7_20_UTE5GCLASSSV344  -  IV_PS_344  -  CV344
#
#    2023-11-20 08:01:21.595854:
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

_du1_pdu_gnb = FPFH(addr="10.0.117.162", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.192", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.193", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.194", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])


_du1_pdu_enb = FPFH(addr="10.0.117.162", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.117.195", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.117.196", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.197", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])

_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQE", 
    ru_hw_group="cMAAr6.1_64T64R", 
    serial_number="1M201311446",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.46", port=5001),  
        ]
    )
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1],
    radio_type="AEQE", 
    ru_hw_group="cMAAr6.1_64T64R", 
    serial_number="1M201204853",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.47", port=5001),  
        ]
    )
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1],
    radio_type="AEQE", 
    ru_hw_group="cMAAr6.1_64T64R", 
    serial_number="1M201304547",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.48", port=5001),  
        ]
    )
)
_shared_rmod_5 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922513",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.49", port=5001),  
        ]
    )
)
_shared_rmod_6 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922515",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.50", port=5001),  
        ]
    )
)
_shared_rmod_7 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2],
    radio_type="AHPMDA", 
    ru_hw_group="FRMr5.1_4T4R", 
    serial_number="K9183922534",
    lmi=SerialOverTcp(
    uart_mapping=[
        Remote(addr="10.14.152.51", port=5001),  
        ]
    )
)
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
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="101",
    product_code="474020B.101",
    rus=[_shared_rmod_5, _shared_rmod_6, _shared_rmod_7],
    serial_number="L1192201065",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_1, _rmod_gnb_2],
    serial_number="L1184208614",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_3],
    serial_number="L1184207649",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="L1200900054",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, 
    global_bts_id=23338, 
    instance_id=720344,
     rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3, _shared_rmod_5, _shared_rmod_7, _shared_rmod_6]
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.49.80", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.80", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.80", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.6.10/29", vlan_id="4003"),
    x2c=NetworkAddress(v4="10.28.6.10/29", vlan_id="4003"),
    x2u=NetworkAddress(v4="10.28.6.10/29", vlan_id="4003"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23338, instance_id=720344)
_realcore = RealCore4G(mcc="540", mnc="01")
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
    rus=[_shared_rmod_5, _shared_rmod_6, _shared_rmod_7, _rmod_enb_7, _rmod_enb_8, _rmod_enb_9],
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
        _shared_rmod_7, 
        _rmod_enb_2, 
        _rmod_enb_3, 
        _rmod_enb_9
    ],
    system_module=_smod_enb_1,
)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.98", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.188", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _du1_pdu_enb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
 ]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_ASIB_3xABIL_3xAHPMDA_3xAEQE_UTECA"

tl = TestLine(
    core=_realcore,
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
