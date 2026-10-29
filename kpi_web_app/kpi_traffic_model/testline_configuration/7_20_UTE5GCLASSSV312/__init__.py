# ##########################################################################################
#
#    7_20_UTE5GCLASSSV312  -  IV_PS_312  -  CV312
#
#    2023-11-17 11:31:31.109575:
#    __init__.py generator (version 1.0 of 21/09/2023).
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

_du1_pdu_gnb = FPFH(addr="10.0.117.163", login="admin", password="admin", port_numbers=[4])
_du1_pdu_enb = FPFH(addr="10.0.117.163", login="admin", password="admin", port_numbers=[3])
_ru1_pdu_gnb = FPFH(addr="10.0.117.170", login="admin", password="admin", port_numbers=[1])
_ru2_pdu_gnb = FPFH(addr="10.0.117.196", login="admin", password="admin", port_numbers=[1])
_ru3_pdu_gnb = FPFH(addr="10.0.117.197", login="admin", password="admin", port_numbers=[1])
_ru4_pdu_gnb = FPFH(addr="10.0.117.165", login="admin", password="admin", port_numbers=[3])
_ru2_pdu_enb = FPFH(addr="10.0.117.165", login="admin", password="admin", port_numbers=[5])
_ru3_pdu_enb = FPFH(addr="10.0.117.195", login="admin", password="admin", port_numbers=[3])
_rmod_gnb_4 = RU(
    pdu_port = _ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="NR_RADIO",
    serial_number="1M201206768",
)
_rmod_gnb_5 = RU(
    pdu_port = _ru2_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="NR_RADIO",
    serial_number="1M201311430",
)
_rmod_gnb_6 = RU(
    pdu_port = _ru3_pdu_gnb.pdu_ports[1],
    radio_type="AEQE",
    ru_hw_group="NR_RADIO",
    serial_number="1M201311447",
)
_shared_rmod_1 = RU(
    pdu_port = _ru4_pdu_gnb.pdu_ports[3],
    radio_type="FRPD",
    ru_hw_group="NR_RADIO",
    serial_number="EA194510739",
)
_rmod_enb_1 = RU(
    pdu_port = _ru2_pdu_enb.pdu_ports[5],
    radio_type="FXED",
    ru_hw_group="NR_RADIO",
    serial_number="F7172209594",
)
_rmod_enb_4 = RU(
    pdu_port = _ru3_pdu_enb.pdu_ports[3],
    radio_type="FRHF",
    ru_hw_group="NR_RADIO",
    serial_number="F7184732976",
)
_fsp_gnb_3 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_6, _rmod_gnb_5],
    serial_number="L1184208560",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="102",
    product_code="474020A.102",
    rus=[_rmod_gnb_4],
    serial_number="L1184409455",
)
_fsp_gnb_1 = CapacityUnit(
    addr="", hardware_type="ABIL", hardware_version="101", product_code="474020B.101", serial_number="L1192201070"
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_3, _fsp_gnb_2, _fsp_gnb_1],
    hardware_type="ASIK",
    hardware_version="474021A.101",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_gnb.pdu_ports[4],
    serial_number="L1184120713",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(
    airscale=_smod_gnb_1,
    global_bts_id=23176,
    instance_id=720312,
    rus=[_rmod_gnb_4, _rmod_gnb_5, _rmod_gnb_6, _shared_rmod_1],
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"), v4="10.14.48.31", vlan_id="1000"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.31", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.31", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.0.102.18/29", vlan_id="4005"),
    x2c=NetworkAddress(v4="10.0.102.17/29", vlan_id="4005"),
    x2u=NetworkAddress(v4="10.0.102.18/29", vlan_id="4005"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23176, instance_id=720312)
_realcore = RealCore4G(mcc="540", mnc="01")
_fsp_enb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="104",
    product_code="473096A.104",
    rus=[_rmod_enb_1, _rmod_enb_4, _shared_rmod_1],
    serial_number="L1192400266",
)
_fct_enb_1 = CommonUnit(
    capacity_units=[_fsp_enb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port = _du1_pdu_enb.pdu_ports[3],
    serial_number="L1190817401",
)
_smod_enb_1 = Airscale(common_units=[_fct_enb_1])
_enb_sbts_1 = RealEnb(
    global_bts_id=22394,
    instance_id=312,
    oam_ip=NetworkAddress(v4="10.14.48.32"),
    rms=[_rmod_enb_1, _rmod_enb_4, _shared_rmod_1],
    system_module=_smod_enb_1,
)
_realcore = RealCore4G(mcc="540", mnc="01")
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_gnb_sbts_1.dus[0].airscale.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.157", password="uteUTE!", port=22, username="ute"),
)
_test_pc_enb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp"),
    ],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.192", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_gnb, _du1_pdu_enb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb, _ru4_pdu_gnb, _ru2_pdu_enb, _ru3_pdu_enb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_NSASA_ASIK_3xABIL_FRPD_3xAEQE_UTECA"

tl = TestLine(
    core=_realcore,
    enbs=[_enb_sbts_1],
    gnbs=[_gnb_sbts_1],
    pdus = _pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_enb_1, _test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
