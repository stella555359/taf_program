# ##########################################################################################
#
#    7_20_UTE4GCLASSSV304  -  IV_PS_304  -  CV304
#
#    2023-11-02 11:07:20
#    __init__.py generator (version 1.0 of 21/09/2023).
#
#    Update: 2025-12-18 14:12
#
# ##########################################################################################

__maintainer__ = "Emmanuel Roger"
__team__ = "MN RAN VRF NPS T01"
__email__ = "emmanuel.roger@nokia.com"

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
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ##############################################################################

cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_du1_pdu_nb = FPFH(addr="10.0.117.152", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_ru1_pdu_nb = FPFH(addr="10.0.96.7", login="admin", password="admin", port_numbers=[1, 2, 3, 4, 5, 6])
_rmod_nb_1 = RU(
    pdu_port=_ru1_pdu_nb.pdu_ports[1], radio_type="FXDD", ru_hw_group="NR_RADIO", serial_number="F7180218054"
)
_fsp_nb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="103",
    product_code="473096A.103",
    rus=[_rmod_nb_1],
    serial_number="L1173607989",
)
_fct_nb_1 = CommonUnit(
    capacity_units=[_fsp_nb_1],
    hardware_type="ASIA",
    hardware_version="473095A.203",
    lmp_connection=SshServiceDetails(addr="192.168.255.129", password="oZPS0POrRieRtu", port=22, username="toor4nsn"),
    pdu_port=_du1_pdu_nb.pdu_ports[5],
    serial_number="L1173502417",
)
_smod_1 = Airscale(common_units=[_fct_nb_1])
_enb_sbts_1 = RealEnb(system_module=_smod_1, rms=[_rmod_nb_1,], oam_ip=NetworkAddress("10.14.49.62"), instance_id=22359,)
_test_pc_nb_1 = TestPc(
    connections=[NetworkAddress(v4="192.168.255.126"), Connection(device=_enb_sbts_1.system_module.common_units[0], interface="eth1", interface_type="lmp")],
    default_ssh_connection_details=SshServiceDetails(addr="10.0.108.193", password="uteUTE!", port=22, username="ute"),
)
_pdus = [_du1_pdu_nb, _ru1_pdu_nb]
_tl_cloud_topology = "CLOUD_SRAN_WG_ASIA_ABIA_FXDD_UTECA"

tl = TestLine(pdus=_pdus, enbs=[_enb_sbts_1], test_pc=_test_pc_nb_1, test_pcs=[_test_pc_nb_1], tl_cloud_topology=_tl_cloud_topology)