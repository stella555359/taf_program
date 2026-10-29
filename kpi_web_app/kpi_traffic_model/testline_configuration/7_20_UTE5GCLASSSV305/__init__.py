# ##########################################################################################
#
#    7_20_UTE5GCLASSSV305  -  IV_PS_305  -  CV305
#
#    2024-06-04 09:18:03.629974:
#    __init__.py generator (version 2.0 of 02/12/2023).
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

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml")

_du1_pdu_gnb = FPFH(addr="10.0.116.145", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.114", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.97.12", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = ATEN(addr="10.14.55.185", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.0.96.7", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.0.97.196", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_4 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="EA204550192"
)
_rmod_gnb_6 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="EA204550197"
)
_rmod_gnb_10 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA205250605"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4], radio_type="AEQE", ru_hw_group="NR_RADIO", serial_number="1M201311427"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4], radio_type="AQQE", ru_hw_group="NR_RADIO", serial_number="L1215205791"
)
_rmod_gnb_12 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA205250592"
)
_rmod_gnb_11 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA205250595"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4], radio_type="AEQE", ru_hw_group="NR_RADIO", serial_number="1M201204844"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="EA204550193"
)
_rmod_gnb_8 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[6], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9183922517"
)
_rmod_gnb_7 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[6], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9184331102"
)
_rmod_gnb_9 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9182521999"
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="104",
    product_code="473096A.104",
    rus=[_rmod_gnb_8, _rmod_gnb_7, _rmod_gnb_9],
    serial_number="DH200293646",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[
        _rmod_gnb_4,
        _rmod_gnb_8,
        _rmod_gnb_12,
        _rmod_gnb_10,
        _rmod_gnb_6,
        _rmod_gnb_9,
        _rmod_gnb_7,
        _rmod_gnb_5,
        _rmod_gnb_11,
    ],
    serial_number="L1223901375",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266B.101",
    rus=[_rmod_gnb_3, _rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_10, _rmod_gnb_6, _rmod_gnb_2],
    serial_number="L1223901376",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[5],
    serial_number="L1201106461",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23267, instance_id=720305)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.49.44", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.44", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.44", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.5.118.178/29", vlan_id="4004"),
    x2c=NetworkAddress(v4="10.5.118.177/29", vlan_id="4004"),
    x2u=NetworkAddress(v4="10.5.118.178/29", vlan_id="4004"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23267, instance_id=720305)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.159", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_SRAN_NLWG_NSASA_ASIB_2xABIO_ABIA_3xAHPMDA_2xAEQE_AQQE_3xAHHB_3xAHEGB_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
