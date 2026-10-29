import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Jiang Hongwei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "hongwei.jiang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.246.75", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Prisma
_airmosaic_ssh = SshServiceDetails(addr="10.57.247.68", username="OTA", password="SQ2")

_airmosaic_harness = HttpConnectionDetails(addr="10.57.247.68", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.247.70", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.247.70", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.57.246.58", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.246.61", port_numbers=[8])

_ru = RU(
    # ru_hw_group='Above6GHz',         # Above6GHz or Below6GHz
    ru_hw_group="AEHA",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.246.83", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = FACOM(addr="10.57.246.58", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=None)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_prisma_ue],
    tl_cloud_topology=_tl_cloud_topology,
)

# compatibility workaround
tl = TestlineWrapper(tl)
