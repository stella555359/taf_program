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
    IperfDataTransferDetails,
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
from taf.config.testline.nms import Netact

__maintainer__ = "xinyu zhang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"  # TL owner's team
__email__ = "sherry.1.zhang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC host(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.133", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.68.87.24", port_numbers=[4])
_ru = RU(
    ru_hw_group="AWHQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.200", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)

_ru_pdu2 = FACOM(addr="10.68.87.24", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AWHQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.199", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)

_ru_pdu3 = FACOM(addr="10.68.87.108", port_numbers=[4])
_ru3 = RU(
    ru_hw_group="AEQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.245", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
)

_ru_pdu4 = FACOM(addr="10.68.87.27", port_numbers=[1])
_ru4 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.45", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu4.pdu_ports[1],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gnb PB
_gnb_pdu = FACOM(addr="10.68.87.60", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2, _ru3, _ru4])

# gnb mplan ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.34", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.48.37", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.68.87.60", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# switch Dtor
# switch port to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.120", port="1/6", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=834)
_netact = Netact("10.108.243.22")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
)
