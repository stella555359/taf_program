# ##########################################################################################
#
#    7_20_UTE5GCLASSSV313_1  -  IV_PS_3_1  -  CV3_1
#
#    2024-01-02 17:31:08.579969:
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

_du1_pdu_gnb = FPFH(addr="10.0.116.226", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_du2_pdu_gnb = FPFH(addr="10.0.116.226", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_du1_pdu_enb = FPFH(addr="10.28.1.106", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.74", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.116.75", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.116.75", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.0.116.73", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.0.116.73", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_gnb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru7_pdu_gnb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru8_pdu_gnb = FPFH(addr="10.0.116.74", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru9_pdu_gnb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru7_pdu_enb = FPFH(addr="10.0.116.72", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru9_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_shared_rmod_8 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="BL2120V0D4F"
)
_shared_rmod_7 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="BL1923V0A8P"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[3], radio_type="AHCA", ru_hw_group="NR_RADIO", serial_number="AS200709144"
)
_shared_rmod_13 = RU(
    pdu_port=_ru4_pdu_gnb.pdu_ports[2], radio_type="AHFIB", ru_hw_group="NR_RADIO", serial_number="K9184615750"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru5_pdu_gnb.pdu_ports[3], radio_type="AHCA", ru_hw_group="NR_RADIO", serial_number="AS200205552"
)
_rmod_gnb_4 = RU(
    pdu_port=_ru6_pdu_gnb.pdu_ports[1], radio_type="AEQK", ru_hw_group="NR_RADIO", serial_number="1M210320686"
)
_rmod_gnb_5 = RU(
    pdu_port=_ru7_pdu_gnb.pdu_ports[1], radio_type="AEQK", ru_hw_group="NR_RADIO", serial_number="1M210320687"
)
_rmod_gnb_2 = RU(
    pdu_port=_ru8_pdu_gnb.pdu_ports[3], radio_type="AHCA", ru_hw_group="NR_RADIO", serial_number="AS200709146"
)
_rmod_gnb_6 = RU(
    pdu_port=_ru9_pdu_gnb.pdu_ports[1], radio_type="AEQK", ru_hw_group="NR_RADIO", serial_number="1M210320689"
)
_rmod_enb_6 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914834"
)
_rmod_enb_1 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="BL2138F1RWG"
)
_rmod_enb_5 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914833"
)
_rmod_enb_2 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="K9183800521"
)
_rmod_enb_4 = RU(
    pdu_port=_ru7_pdu_enb.pdu_ports[3], radio_type="AHNA", ru_hw_group="NR_RADIO", serial_number="AS212914831"
)
_rmod_enb_3 = RU(
    pdu_port=_ru9_pdu_enb.pdu_ports[2], radio_type="AHLBA", ru_hw_group="NR_RADIO", serial_number="K9183800520"
)
_fsp_gnb_6 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_6],
    serial_number="L1191006909",
)
_fsp_gnb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_4],
    serial_number="L1183403123",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="101",
    product_code="474020B.101",
    rus=[_shared_rmod_13],
    serial_number="L1193416817",
)
_fsp_gnb_5 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_5],
    serial_number="L1183403067",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="101",
    product_code="474020B.101",
    rus=[_shared_rmod_7, _shared_rmod_8],
    serial_number="L1193416784",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="101",
    product_code="474020B.101",
    rus=[_rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_1],
    serial_number="L1191902556",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_3, _fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIK",
    hardware_version="474021A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="EA194555716",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[_fsp_gnb_6, _fsp_gnb_4, _fsp_gnb_5],
    hardware_type="ASIK",
    hardware_version="474021A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du2_pdu_gnb.pdu_ports[5],
    serial_number="EA193954736",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23291, instance_id=720313)
_du_2 = DU(airscale=_smod_gnb_2, global_bts_id=23291, instance_id=720313)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.24", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.24", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.24", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c313:4005:3/112", vlan_id="4003"),
    x2c=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c313:4005:2/112", vlan_id="4003"),
    x2u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c313:4005:2/112", vlan_id="4003"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23291, instance_id=720313)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=23291, instance_id=720313, master=_gnb_sbts_1)
_gnb_sbts_1.slave = _gnb_sbts_2
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_13, _shared_rmod_8, _shared_rmod_7],
    serial_number="EA192071772",
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_5, _rmod_enb_6, _rmod_enb_4],
    serial_number="L1182601815",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2],
    serial_number="EA190473657",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_3, _fsp_enb_2, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[2],
    serial_number="RW192202804",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22297,
    instance_id=313,
    oam_ip=NetworkAddress(v4="10.14.48.23"),
    rms=[
        _rmod_enb_1,
        _rmod_enb_3,
        _rmod_enb_2,
        _rmod_enb_5,
        _rmod_enb_6,
        _rmod_enb_4,
        _shared_rmod_13,
        _shared_rmod_8,
        _shared_rmod_7,
    ],
    system_module=_smod_enb_1,
)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.151", password="uteUTE!", port=22, username="ute"),
)
_test_pc_gnb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.119"),
        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.169", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.119", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _du2_pdu_gnb,
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
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
    _ru4_pdu_enb,
    _ru7_pdu_enb,
    _ru9_pdu_enb,
]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_2xASIK_6xABIL_3xAEQK_3xAHFIB_3xAHCA_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
