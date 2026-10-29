# ##########################################################################################
#
#    7_20_UTE5GCLASSSV307  -  IV_PS_307  -  CV307
#
#    2023-12-17 22:19:53.954166:
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
os.environ["INIT_CONFIG_FILE_PATH"] = cfg_dir
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(cfg_dir, "ue_config.yaml")

__all__ = ["tl"]

_du1_pdu_gnb = FPFH(
    addr="10.0.117.83", login="admin", password="admin", port_numbers=[6]
)
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.160", login="admin", password="admin", port_numbers=[3]
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.139", login="admin", password="admin", port_numbers=[3]
)
_ru3_pdu_gnb = FPFH(
    addr="10.0.117.160", login="admin", password="admin", port_numbers=[2]
)
_rmod_gnb_3 = RU(
    pdu_port=_ru3_pdu_gnb.pdu_ports[2],
    radio_type="ARPA",
    ru_hw_group="NR_RADIO",
    serial_number="F7202501497",
)
_rmod_gnb_2 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[3],
    radio_type="AZQS",
    ru_hw_group="NR_RADIO",
    serial_number="4H210430143",
)
_rmod_gnb_1 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[3],
    radio_type="AZQO",
    ru_hw_group="NR_RADIO",
    serial_number="1M203800596",
)
_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_2, _rmod_gnb_1],
    # rus=[_rmod_gnb_2, _rmod_gnb_1, _rmod_gnb_3],
    serial_number="L1204104683",
)
_fct_gnb_1 = CommonUnit(
    capacity_units=[_fsp_gnb_1],
    hardware_type="ASIB",
    hardware_version="473764A.102",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    pdu_port=_du1_pdu_gnb.pdu_ports[6],
    serial_number="L1203700089",
)
_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])
_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23362, instance_id=307)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        routing_v4=RoutingInformation(gateway="110.14.49.254/0"),
        v4="10.14.49.77",
        vlan_id="1000",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.77", password="nemuuser", port=443, username="Nemuadmin"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.77", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    s1u=NetworkAddress(v4="10.28.11.122/29", vlan_id="4003"),
    x2c=NetworkAddress(v4="10.28.11.121/29", vlan_id="4003"),
    x2u=NetworkAddress(v4="10.28.11.122/29", vlan_id="4003"),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23362, instance_id=307)
_test_pc_gnb_1 = TestPc(
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(
            device=_gnb_sbts_1.dus[0].airscale.common_units[0],
            interface="eth1",
            interface_type="lmp",
        ),
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.67", password="uteUTE!", port=22, username="ute"
    ),
)
_pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb]
# _pdus = [_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb, _ru3_pdu_gnb]
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIB_ABIO_AZQS_AZQO_UTECA"

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=_pdus,
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology=_tl_cloud_topology,
)
