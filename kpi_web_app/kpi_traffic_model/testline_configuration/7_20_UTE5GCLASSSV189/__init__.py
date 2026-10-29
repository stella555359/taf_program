# ##########################################################################################
#
#    7_20_UTE5GCLASSSV189  -  IV_PS_189  -  CV189
#
#    2024-01-24 15:49:38.576118:
#    __init__.py generator (version 2.0 of 02/12/2023).
#
# ##########################################################################################

__maintainer__ = "Youssef Leulmi"
__team__ = "MN RAN VRF NPS"
__email__ = "youssef.leulmi@nokia.com"

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
from taf.config.testline.attenuator import Hytem

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #
os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

__all__ = ["tl"]

_attenuator0 = Hytem(
    ip_addr="10.0.96.123", port=10001, attenuation_port_numbers=[0, 1, 2, 3, 4, 5, 6, 7]
)
_du1_pdu_gnb = FPFH(addr="10.0.117.84", login="admin", password="admin", port_numbers=[4])
_ru1_pdu_gnb = FPFH(
    addr="10.0.117.139", login="admin", password="admin", port_numbers=[1]
)
_rmod_gnb_1 = RU(
    pdu_port=_ru1_pdu_gnb.pdu_ports[1],
    radio_type="AEQN",
    ru_hw_group="NR_RADIO",
    serial_number="CV193201178",
    attenuation_ports=[
        _attenuator0.attenuator_ports[2],
        _attenuator0.attenuator_ports[3],
    ],
)
_ru2_pdu_gnb = FPFH(
    addr="10.0.117.139", login="admin", password="admin", port_numbers=[2]
)
_rmod_gnb_2 = RU(
    pdu_port=_ru2_pdu_gnb.pdu_ports[2],
    ru_hw_group="NR_RADIO",
    radio_type="AHLOA",
    serial_number="K9182103377",
    attenuation_ports=[
        _attenuator0.attenuator_ports[6],
        _attenuator0.attenuator_ports[7],
    ],
)

_fsp_gnb_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_1],
    serial_number="L1204109022",
)
_fsp_gnb_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="101",
    product_code="475266A.101",
    rus=[_rmod_gnb_2],
    serial_number="L1204008468",
)
_du2_asik_master_L = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_asik_slave_L = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_capacity_unit_L_0 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1a", hardware_type="ABIO")
_du2_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1b", hardware_type="ABIO")
_du2_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1c", hardware_type="ABIO")
_du2_capacity_unit_L_1 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIO")
_du2_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-2a", hardware_type="ABIO")
_du2_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-2b", hardware_type="ABIO")
_du2_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-2c", hardware_type="ABIO")

_fct_gnb_1 = CommonUnit(
    hardware_type="ASIM",
    hardware_version="475765A.Y13",
    serial_number="L1223306795",
    lmp_connection=SshServiceDetails(
        addr="10.14.49.164", password="oZPS0POrRieRtu", port=22, username="toor4nsn"
    ),
    capacity_units=[
        _du2_asik_master_L,
        _du2_asik_slave_L,
        _du2_capacity_unit_L_0,
        _du2_master_capacity_unit_L_0,
        _du2_slave_capacity_unit_L_0,
        _du2_fpga_capacity_unit_L_0,
        _du2_capacity_unit_L_1,
        _du2_master_capacity_unit_L_1,
        _du2_slave_capacity_unit_L_1,
        _du2_fpga_capacity_unit_L_1,
    ],
    pdu_port=_du1_pdu_gnb.pdu_ports[4],
)

_smod_gnb_1 = Airscale(common_units=[_fct_gnb_1])


_du_1 = DU(airscale=_smod_gnb_1, global_bts_id=23212, instance_id=189)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.49.164",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.164", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4="10.28.11.65", vlan_id=4003),
    x2u=NetworkAddress(v4="10.28.11.66", vlan_id=4003),
    s1u=NetworkAddress(v4="10.28.11.66", vlan_id=4003),
)
_gnb_sbts_1 = ClassicalBts(cu=_cu, dus=[_du_1], global_bts_id=23212, instance_id=189)

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
        addr="10.0.108.137",
        password="uteUTE!",
        port=22,
        username="ute",
    ),
)

tl = TestLine(
    gnbs=[_gnb_sbts_1],
    pdus=[_du1_pdu_gnb, _ru1_pdu_gnb, _ru2_pdu_gnb],
    test_pc=_test_pc_gnb_1,
    test_pcs=[_test_pc_gnb_1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASIM_2xABIO_AEQN_AHLOA_UTECA",
)
