__maintainer__ = "Xiaping Zhang"
__team__ = "MN_RAN_L2_SW_1_CN_06_SG"
__email__ = "I_EXT_MN_RAN_L2_SW_1_CN_06_SG@internal.nsn.com"
__owner_email__ = "xiaping.zhang@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.ue import Prisma
from taf.config.testline.enb import PrismaEnb
from taf.config.testline.core import PrismaCore
from taf.config.testline.pdu import HBTE


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.215.26", username="ute", password="ute"
    )
)

_pdu1 = HBTE(addr="10.68.87.44", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdu2 = HBTE(addr="10.68.87.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu1, _pdu2]

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="10.68.88.101", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[1],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.101", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.101", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=2221),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=2221),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=2221),
)

_ru1 = RU(
    ru_hw_group="AEHC",
    radio_type=RadioTypes.AEHC,
    pdu_port=_pdus[1].pdu_ports[1],
)

_ru2 = RU(
    ru_hw_group="AEHC",
    radio_type=RadioTypes.AEHC,
    pdu_port=_pdus[1].pdu_ports[2],
)

_du = DU(airscale=_airscale, rus=[_ru1, _ru2])

_cbts = ClassicalBts(cu=_cu, dus=[_du])


_airmosaic_ssh = SshServiceDetails(addr='10.101.47.219', username='nokia5G', password='noki@123')
_airmosaic_harness = HttpConnectionDetails(addr='10.101.47.219', port=8090)

_lsu_uu_ssh = SshServiceDetails(addr='10.68.88.105', username='user', password='user')
_tstm_uu_ssh = SshServiceDetails(addr='10.68.88.105', username='user', password='user')
 
_prisma_ue =  Prisma(airmosaic_ssh_connection_details=_airmosaic_ssh,
                 airmosaic_harness_connection_details=_airmosaic_harness,
                 lsu_uu_ssh_connection_details=_lsu_uu_ssh,
                 tstm_uu_ssh_connection_details=_tstm_uu_ssh
                 )
_lsu_s1_ssh = SshServiceDetails(addr='10.68.88.105', username='user', password='user')
_tstm_s1_ssh = SshServiceDetails(addr='10.68.88.105', username='user', password='user')
_prisma_core = PrismaCore(
                 lsu_s1_ssh_connection_details=_lsu_s1_ssh, 
                 tstm_s1_ssh_connection_details=_tstm_s1_ssh)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="Real_5G_CLASSICAL_Prisma",
    ues=[_prisma_ue],
    core=_prisma_core,
    pdus=_pdus,
)

__all__ = ["tl"]
