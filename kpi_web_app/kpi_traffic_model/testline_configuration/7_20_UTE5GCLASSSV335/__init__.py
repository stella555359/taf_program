# ##########################################################################################
#
#    7_20_UTE5GCLASSSV335_1  -  IV_PS_5_1  -  CV5_1
#
#    2023-12-05 19:28:31.092101:
#    __init__.py generator (version 2.0 of 02/12/2023).
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

_du1_pdu_gnb = FPFH(addr="10.0.117.96", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_du2_pdu_gnb = FPFH(addr="10.0.117.96", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_du1_pdu_enb = FPFH(addr="10.0.117.96", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.188", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_gnb = FPFH(addr="10.0.117.189", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu_gnb = FPFH(addr="10.0.117.190", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu_gnb = FPFH(addr="10.0.117.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru2_pdu_enb = FPFH(addr="10.0.117.187", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru3_pdu_enb = FPFH(addr="10.0.117.186", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru4_pdu_enb = FPFH(addr="10.0.117.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru5_pdu_enb = FPFH(addr="10.0.117.191", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru6_pdu_enb = FPFH(addr="10.0.117.190", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
#_ru9_pdu_enb = FPFH(addr="10.0.117.189", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_4 = RU(
    pdu_port = _ru6_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M210320688",
)
_rmod_gnb_2 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="AS195003431",
)
_rmod_gnb_6 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M211917767",
)
_rmod_gnb_5 = RU(
    pdu_port = _ru5_pdu_gnb.pdu_ports[4],
    radio_type="AEQK",
    ru_hw_group="NR_RADIO",
    serial_number="1M211917768",
)
_shared_rmod_15 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGUN",
)
_rmod_gnb_3 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="AS195003435",
)
_rmod_gnb_1 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[6],
    radio_type="AHCA",
    ru_hw_group="NR_RADIO",
    serial_number="AS195003430",
)
_shared_rmod_13 = RU(
    pdu_port = _ru6_pdu_gnb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGWY",
)
_shared_rmod_14 = RU(
    pdu_port = _ru5_pdu_gnb.pdu_ports[5],
    radio_type="UHIE",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD19120YGXT",
)
_shared_rmod_7 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWLU",
)
_shared_rmod_8 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWMG",
)
_shared_rmod_9 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[4],
    radio_type="UHFA",
    ru_hw_group="NR_RADIO",
    serial_number="LBALLU-YD18090RWML",
)
_rmod_enb_14 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182107374",
)
_rmod_enb_10 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182614353",
)
_rmod_enb_11 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914830",
)
_rmod_enb_15 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[5],
    radio_type="AHLBA",
    ru_hw_group="NR_RADIO",
    serial_number="K9182614354",
)
_rmod_enb_12 = RU(
    pdu_port = _ru5_pdu_gnb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914827",
)
_rmod_enb_13 = RU(
    pdu_port = _ru6_pdu_gnb.pdu_ports[6],
    radio_type="AHNA",
    ru_hw_group="NR_RADIO",
    serial_number="AS212914829",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_shared_rmod_13, _shared_rmod_15, _shared_rmod_14],
    serial_number="L1184321635",
)
_fsp_gnb_6 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_6],
    serial_number="L1183315438",
)
_fsp_gnb_5 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_5],
    serial_number="L1184208633",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_shared_rmod_8, _shared_rmod_9, _shared_rmod_7],
    serial_number="L1184321633",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_1, _rmod_gnb_2, _rmod_gnb_3],
    serial_number="L1185109701",
)
_fsp_gnb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_4],
    serial_number="L1184321637",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_2, _fsp_gnb_3, _fsp_gnb_1],
    hardware_type="ASIK",
    hardware_version="474021A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[2],
    serial_number="L1201004552",
)
_fct_gnb_2 = CommonUnit(
    capacity_units=[_fsp_gnb_6, _fsp_gnb_5, _fsp_gnb_4],
    hardware_type="ASIK",
    hardware_version="474021A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.7", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[1],
    serial_number="L1201004556",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_smod_gnb_2 = Airscale(common_units=[_fct_gnb_2])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23323, instance_id=720335)
_du_2 = DU(airscale=_smod_gnb_2, global_bts_id=23323, instance_id=720335)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.120", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.120", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.120", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c335:4002:3/112", vlan_id="4001"),
    x2c=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c335:4002:2/112", vlan_id="4001"),
    x2u=NetworkAddress(v4="2a00:8a00:40ff:c000:2:c335:4002:2/112", vlan_id="4001"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23323, instance_id=720335)
_gnb_sbts_2 = ClassicalBts(cu=_cu, dus=[_du_2], global_bts_id=23323, instance_id=720335, master=_gnb_sbts_1)
_gnb_sbts_1.slave = _gnb_sbts_2
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_shared_rmod_15, _shared_rmod_13, _shared_rmod_14],
    serial_number="EA192178938",
)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_15, _shared_rmod_14, _rmod_enb_10],
    serial_number="EA192178885",
)
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_13, _shared_rmod_14, _rmod_enb_12, _shared_rmod_8, _rmod_enb_11, _shared_rmod_9],
    serial_number="EA192178820",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_3, _fsp_enb_2, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.204",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[4],
    serial_number="L1201109779",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22331,
    instance_id=22331,
    oam_ip=NetworkAddress(v4="10.14.48.119"),
    rms=[
        _rmod_enb_13,
        _shared_rmod_7,
        _rmod_enb_12,
        _shared_rmod_8,
        _rmod_enb_11,
        _shared_rmod_9,
        _rmod_enb_14,
        _rmod_enb_15,
        _rmod_enb_10,
        _shared_rmod_15,
        _shared_rmod_13,
        _shared_rmod_14,
    ],
    system_module=_smod_enb_1,
)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.175", password="uteUTE!", port=22, username="ute"),
)
_test_pc_gnb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.7"),
        Connection(device=_gnb_sbts_2.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.176", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.121", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru4_pdu_gnb,
    _ru5_pdu_gnb,
    _ru6_pdu_gnb,
]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_2xASIK_6xABIL_3xUHFA_3xAEQK_3xUHIE_3xAHCA_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1, _gnb_sbts_2],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1, _test_pc_gnb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
