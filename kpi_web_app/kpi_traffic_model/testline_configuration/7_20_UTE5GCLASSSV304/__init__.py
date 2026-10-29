# ##########################################################################################
#
#    7_20_UTE5GCLASSSV304  -  IV_PS_304  -  CV304
#
#    2025-12-18 14:21:
#    __init__.py generator (version 2.4 of 03/07/2024).
#
# ##########################################################################################

__maintainer__ = "A NEZROUK"
__team__ = "MN RAN VRF NPS T02"
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
from collections import OrderedDict
from taf.config.testline.gnb.du import Cablink, Endpoint

# ##############################################################################
#                                                                              #
#                          TL standard definition                              #
#                                                                              #
# ##############################################################################

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]


_du1_pdu_gnb = FPFH(addr="10.0.117.152", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.97.196", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.116.114", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.97.12", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.0.96.7", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.0.116.78", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])


_rmod_gnb_11 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[3], radio_type="AHPD", ru_hw_group="NR_RADIO", serial_number="6Q184907608"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3], radio_type="FRHG", ru_hw_group="NR_RADIO", serial_number="K9162601053"
)
_rmod_gnb_10 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[2], radio_type="AHPD", ru_hw_group="NR_RADIO", serial_number="6Q184907597"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[1], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M203816968"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M202227575"
)
_rmod_gnb_12 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2], radio_type="FRMF", ru_hw_group="NR_RADIO", serial_number="F7175112523"
)
_rmod_gnb_6 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3], radio_type="FRHG", ru_hw_group="NR_RADIO", serial_number="K9174573585"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[3], radio_type="FRHG", ru_hw_group="NR_RADIO", serial_number="K9174047497"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[1], radio_type="AEQQ", ru_hw_group="NR_RADIO", serial_number="1M204112636"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[3], radio_type="AHPD", ru_hw_group="NR_RADIO", serial_number="6Q184907604"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2], radio_type="FRGU", ru_hw_group="NR_RADIO", serial_number="AS175012077"
)
_rmod_gnb_7 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2], radio_type="FXED", ru_hw_group="NR_RADIO", serial_number="1M201420735"
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_11, _rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9, _rmod_gnb_10],
    serial_number="L1224009391",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_3, _rmod_gnb_6, _rmod_gnb_2, _rmod_gnb_11, _rmod_gnb_4, _rmod_gnb_5],
    serial_number="L1224009384",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_gnb_4, _rmod_gnb_6, _rmod_gnb_12, _rmod_gnb_5],
    serial_number="L1173606477",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_1, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="L1202903923",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23349, instance_id=23349)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="10.14.49.254/0"), v4="10.14.49.68", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.68", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.68", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.16.98/32"),
    x2c=NetworkAddress(v4="10.28.16.97/32"),
    x2u=NetworkAddress(v4="10.28.16.98/32"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23349, instance_id=23349)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.156", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_SRAN_NL_NSASA_ASIB_2xABIO_ABIA_FXED_FRGU_3xAEQQ_FRMF_3xAHPD_3xFRHG_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
