# ##########################################################################################
#
#    7_20_UTE5GCLASSSV343  -  IV_PS_343  -  CV343
#
#    2024-06-20 12:17:28.216275:
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

_du1_pdu_gnb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_du1_pdu_enb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_du2_pdu_enb = FPFH(addr="10.0.117.97", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_gnb = FPFH(addr="10.0.116.254", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_gnb = FPFH(addr="10.0.116.255", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_gnb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_enb = FPFH(addr="10.0.116.254", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu_enb = FPFH(addr="10.0.116.255", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu_enb = FPFH(addr="10.0.117.0", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu_enb = FPFH(addr="10.0.117.98", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[4], radio_type="AEQE", ru_hw_group="NR_RADIO", serial_number="1M213011749"
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[4], radio_type="AEQE", ru_hw_group="NR_RADIO", serial_number="1M213011772"
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[4], radio_type="AEQE", ru_hw_group="NR_RADIO", serial_number="1M213011702"
)
_rmod_enb_4 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381647"
)
_rmod_enb_5 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381642"
)
_rmod_enb_1 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[4], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="EA222752596"
)
_rmod_enb_3 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[6], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9182709936"
)
_rmod_enb_9 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9181925280"
)
_rmod_enb_6 = RU(
    pdu_port=_ru3_pdu_enb.pdu_ports[6], radio_type="AHHB", ru_hw_group="NR_RADIO", serial_number="EA184381645"
)
_rmod_enb_2 = RU(
    pdu_port=_ru4_pdu_enb.pdu_ports[5], radio_type="AHPMDA", ru_hw_group="NR_RADIO", serial_number="K9181625747"
)
_rmod_enb_8 = RU(
    pdu_port=_ru2_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9193933072"
)
_rmod_enb_7 = RU(
    pdu_port=_ru1_pdu_enb.pdu_ports[5], radio_type="AHEGB", ru_hw_group="NR_RADIO", serial_number="K9181925259"
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="102",
    product_code="475266A.102",
    rus=[_rmod_gnb_2, _rmod_gnb_3, _rmod_gnb_1],
    serial_number="L1204506029",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_gnb.pdu_ports[5],
    serial_number="DH213033729",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23286, instance_id=720343)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.69", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.69", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.69", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.102.122/29", vlan_id="4006"),
    x2c=NetworkAddress(v4="10.0.102.121/29", vlan_id="4006"),
    x2u=NetworkAddress(v4="10.0.102.122/29", vlan_id="4006"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23286, instance_id=720343)
_fsp_enb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2],
    serial_number="L1172902335",
)
_fsp_enb_5 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="EA192178830"
)
_fsp_enb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_6, _rmod_enb_4, _rmod_enb_5],
    serial_number="L1173607987",
)
_fsp_enb_1 = CapacityUnit(
    addr="", hardware_type="ABIA", hardware_version="103", product_code="473096A.103", serial_number="K9172529981"
)
_fsp_enb_4 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_enb_9, _rmod_enb_7, _rmod_enb_8],
    serial_number="EA192178866",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_2, _fsp_enb_3, _fsp_enb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_enb.pdu_ports[4],
    serial_number="L1212115869",
)
_fct_enb_2 = CommonUnit(
    capacity_units=[_fsp_enb_5, _fsp_enb_4],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.119", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du2_pdu_enb.pdu_ports[3],
    serial_number="L1173422528",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_smod_enb_2 = Airscale(common_units=[_fct_enb_2])
_enb_sbts_1 = RealEnb(
    global_bts_id=23322,
    instance_id=343,
    oam_ip=NetworkAddress(v4="10.14.48.68"),
    rms=[_rmod_enb_1, _rmod_enb_3, _rmod_enb_2, _rmod_enb_6, _rmod_enb_4, _rmod_enb_5],
    system_module=_smod_enb_1,
)
_enb_sbts_2 = RealEnb(master=_enb_sbts_1, rms=[_rmod_enb_9, _rmod_enb_7, _rmod_enb_8], system_module=_smod_enb_2)
_enb_sbts_1.slave = _enb_sbts_2
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.161", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.118", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_2 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_2.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.189", password="uteUTE!", port=22, username="ute"),
)
_pdus = [
    _du1_pdu_gnb,
    _du1_pdu_enb,
    _du2_pdu_enb,
    _ru1_pdu_gnb,
    _ru2_pdu_gnb,
    _ru3_pdu_gnb,
    _ru1_pdu_enb,
    _ru2_pdu_enb,
    _ru3_pdu_enb,
    _ru4_pdu_enb,
]
#_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSA_ASIB_ABIO_3xAEQE_UTECA"
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSA_ASIKA_ABIL_3xAHCA_UTECA"

tl = TestLine(
    enbs=[_enb_sbts_1, _enb_sbts_2],
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1, _test_pc_enb_2],
    tl_cloud_topology=_tl_cloud_topology,
)
