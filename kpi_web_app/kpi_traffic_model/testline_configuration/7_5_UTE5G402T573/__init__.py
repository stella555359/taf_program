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
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact

__maintainer__ = "Li Mengting"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com"  # TL owner's team
__email__ = "mengting.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu = FACOM(addr="10.57.241.147", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.142", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)


# classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.57.241.142", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru])

# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.130", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.235.139", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.241.142", port_numbers=[3])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[3],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# switch Dtor
# switch port to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.215", port="1/3", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=573)
# netact ip
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)

tl = TestlineWrapper(tl)
