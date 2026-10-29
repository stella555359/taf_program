# ##########################################################################################
#
#    7_20_UTE5GCLASSSV331  -  IV_PS_331  -  CV331
#
#    2023-12-04 21:40:08.729378:
#    __init__.py generator (version 1.0 of 21/09/2023).
#
# ##########################################################################################

__maintainer__ = "A NEZROUK"
__team__ = "MN RAN Pz NPS SG2"
__email__ = "Abderrahmane.nezrouk@nokia.com"

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

_du1_pdu_gnb = FPFH(addr="10.0.117.112", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.28.1.87", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.28.1.85", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.28.1.86", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.28.1.86", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.28.1.85", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_gnb = FPFH(addr="10.0.117.184", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_2 = RU(
   # ok verifie correspond a RMOD-2 AZQU 4H210630109 http://10.28.1.87/ output 5
    pdu_port = _ru1_pdu_gnb.pdu_ports[5],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630109",
)
_rmod_gnb_6 = RU(
    # ok verifie correspond a RMOD-6 AZQU 4H210630073 http://10.28.1.85/ output 6
    pdu_port = _ru2_pdu_gnb.pdu_ports[6],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630073",
)
_rmod_gnb_3 = RU(
    # ok verifie correspond a RMOD-3 AZQU 4H210630103 http://10.28.1.86/ output 5
    pdu_port = _ru3_pdu_gnb.pdu_ports[5],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630103",
)
_rmod_gnb_5 = RU(
   # ok verifie correspond a RMOD-5 AZQU 4H210630060 http://10.28.1.86/ output 6
    pdu_port = _ru4_pdu_gnb.pdu_ports[6],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630060",
)
_rmod_gnb_4 = RU(
    # ok verifie correspond a RMOD-4 RMOD-4 4H210630068 http://10.28.1.85/ output 5
    pdu_port = _ru5_pdu_gnb.pdu_ports[5],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630068",
)
_rmod_gnb_1 = RU(
    # ok verifie correspond a RMOD-1 AZQU 4H210630070 http://10.0.117.184/ output5
    pdu_port = _ru6_pdu_gnb.pdu_ports[5],
    radio_type="AZQU",
    ru_hw_group="NR_RADIO",
    serial_number="4H210630070",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="103",
    product_code="474824A.103",
    rus=[_rmod_gnb_4, _rmod_gnb_3],
    serial_number="L1220306585",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="103",
    product_code="474824A.103",
    rus=[_rmod_gnb_2, _rmod_gnb_1],
    serial_number="L1220306584",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="103",
    product_code="474824A.103",
    rus=[_rmod_gnb_5, _rmod_gnb_6],
    serial_number="L1220306586",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_1, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    # ok verifie complete
    pdu_port = _du1_pdu_gnb.pdu_ports[4],
    serial_number="DH200762395",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=331,
    instance_id=331,
    rus=[_rmod_gnb_2, _rmod_gnb_6, _rmod_gnb_3, _rmod_gnb_5, _rmod_gnb_4, _rmod_gnb_1],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.0.115.254/0"), v4="10.0.114.46", vlan_id="1005"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.114.46", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.114.46", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.112.185/29", vlan_id="4002"),
    x2c=NetworkAddress(v4="10.0.112.186/29", vlan_id="4002"),
    x2u=NetworkAddress(v4="10.0.112.185/29", vlan_id="4002"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=331, instance_id=331)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.138", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb, _ru4_pdu_gnb, _ru5_pdu_gnb, _ru6_pdu_gnb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSA_ASIB_3xABIN_6xAZQU_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
