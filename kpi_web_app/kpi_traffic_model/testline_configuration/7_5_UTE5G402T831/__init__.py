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
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "yin.4.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.97", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_pdu = FACOM(addr="10.68.87.110", port_numbers=[1])
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_pdu2 = FACOM(addr="10.68.87.110", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.27', username='root', password='nokia123'),
    pdu_port=_ru_pdu2.pdu_ports[2],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.68.87.107", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2], f1_m_ip_addr="10.68.88.246")

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.246", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.246", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_pdu = FACOM(addr="10.68.87.106", port_numbers=[7])
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.89.9", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[7],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=831, global_bts_id=831)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
)
