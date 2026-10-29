# ##########################################################################################
#
#    7_20_UTE5GCLASSSV336  -  IV_PS_336  -  CV336
#
#    2023-12-04 15:57:08.220678:
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

_du1_pdu_gnb = FPFH(addr="10.0.116.226", login="admin", password="admin", port_numbers=[2])
_du1_pdu_enb = FPFH(addr="10.0.116.226", login="admin", password="admin", port_numbers=[4])
_ru1_pdu_gnb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[5])
_ru2_pdu_gnb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.201", login="admin", password="admin", port_numbers=[6])
_ru4_pdu_gnb = FPFH(addr="10.0.117.198", login="admin", password="admin", port_numbers=[6])
_ru5_pdu_gnb = FPFH(addr="10.0.117.199", login="admin", password="admin", port_numbers=[6])
_ru6_pdu_gnb = FPFH(addr="10.0.117.200", login="admin", password="admin", port_numbers=[6])
_ru7_pdu_gnb = FPFH(addr="10.0.117.198", login="admin", password="admin", port_numbers=[4])
_ru8_pdu_gnb = FPFH(addr="10.0.117.199", login="admin", password="admin", port_numbers=[4])
_ru9_pdu_gnb = FPFH(addr="10.0.117.200", login="admin", password="admin", port_numbers=[4])
_ru13_pdu_gnb = FPFH(addr="10.0.117.201", login="admin", password="admin", port_numbers=[4])
_ru14_pdu_gnb = FPFH(addr="10.0.117.202", login="admin", password="admin", port_numbers=[4])
_ru15_pdu_gnb = FPFH(addr="10.0.117.198", login="admin", password="admin", port_numbers=[5])
_shared_rmod_1 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[5],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2234N41L4",
)
_shared_rmod_2 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[6],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2222N407P",
)
_shared_rmod_3 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[6],
    radio_type="AHFII",
    ru_hw_group="NR_RADIO",
    serial_number="BL2234N41KG",
)
_rmod_gnb_4 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="AS200205532",
)
_rmod_gnb_5 = RU(
    pdu_port = _ru5_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="1M190819379",
)
_rmod_gnb_6 = RU(
    pdu_port = _ru6_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="1M190429343",
)
_rmod_gnb_7 = RU(
    pdu_port = _ru7_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M211917765",
)
_rmod_gnb_8 = RU(
    pdu_port = _ru8_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M211917770",
)
_rmod_gnb_9 = RU(
    pdu_port = _ru9_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M211917771",
)
_rmod_gnb_13 = RU(
    pdu_port = _ru13_pdu_gnb.pdu_ports[4],
    radio_type="AEQU",
    ru_hw_group="NR_RADIO",
    serial_number="1M220600979",
)
_rmod_gnb_14 = RU(
    pdu_port = _ru14_pdu_gnb.pdu_ports[4],
    radio_type="AEQU",
    ru_hw_group="NR_RADIO",
    serial_number="1M220600980",
)
_rmod_gnb_15 = RU(
    pdu_port = _ru15_pdu_gnb.pdu_ports[5],
    radio_type="AEQU",
    ru_hw_group="NR_RADIO",
    serial_number="1M220600972",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_shared_rmod_1, _shared_rmod_2, _shared_rmod_3, _rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6],
    serial_number="L1204109006",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_7, _rmod_gnb_8, _rmod_gnb_9],
    serial_number="L1204008466",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_13, _rmod_gnb_14, _rmod_gnb_15],
    serial_number="L1204104635",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1, _fsp_gnb_2, _fsp_gnb_3],
    hardware_type="ASIL",
    hardware_version="474767A.101",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[2],
    serial_number="DH222244769",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=23332,
    instance_id=720336,
    rus=[
        _shared_rmod_1,
		_shared_rmod_2,
		_shared_rmod_3,
        _rmod_gnb_4,
		_rmod_gnb_5,
        _rmod_gnb_6,
        _rmod_gnb_7,
        _rmod_gnb_8,
        _rmod_gnb_9,
        _rmod_gnb_13,
        _rmod_gnb_14,
        _rmod_gnb_15,
    ],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.108", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.108", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.108", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c336:4003:3/112", vlan_id="4001"),
    x2c=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c336:4003:2/112", vlan_id="4001"),
    x2u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c336:4003:2/112", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23332, instance_id=720336)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="EA192178804"
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_1, _shared_rmod_3, _shared_rmod_2],
    serial_number="L1173619560",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1, _fsp_enb_2],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[4],
    serial_number="L1171800899",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22339,
    instance_id=22339,
    oam_ip=NetworkAddress(v4="10.14.48.118"),
    rms=[_shared_rmod_1, _shared_rmod_3, _shared_rmod_2],
    system_module=_smod_enb_1,
)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.164", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.190", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _du1_pdu_enb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
    _ru6_pdu_gnb,
    _ru7_pdu_gnb,
    _ru8_pdu_gnb,
    _ru9_pdu_gnb,
    _ru13_pdu_gnb,
    _ru14_pdu_gnb,
    _ru15_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_ASIL_3xABIO_3xAEQU_3xAHCA_3xAEQK_3xAHFII_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
