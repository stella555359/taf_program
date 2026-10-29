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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android

__maintainer__ = "Xing Pan"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "casbo.xing@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# classical gNB LMP
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.30", username="root", password="nokia123"
    )
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.241.225", port_numbers=[2])

_ru = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.167.30", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)


# gNB MPlane IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# abil internal IP
_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.57.241.197", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru])

# gNB MPlane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.229.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.229.133", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.237.144", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.241.224", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

## switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.215", port="1/3", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


# instance_id=MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=89)

# Netact IP
_netact = Netact("10.107.178.214")


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    # core=_epcsim,
    switches=[_dell_s4048on_switch],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)

tl = TestlineWrapper(tl)
