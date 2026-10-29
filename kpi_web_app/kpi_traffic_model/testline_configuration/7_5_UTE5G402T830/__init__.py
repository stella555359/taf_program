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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Wang Dali"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "dali.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# PB for RU

_ru_pdu1 = FACOM(addr="10.68.87.102", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2114G1A9D",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu1.pdu_ports[2],
)

_ru_pdu2 = FACOM(addr="10.68.87.104", port_numbers=[4])
_ru2 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2048G1RBY",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
)

_ru_pdu3 = FACOM(addr="10.68.87.104", port_numbers=[1])
_ru3 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2039G1M0L",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[1],
)


# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = HBTE(addr="10.68.87.107", port_numbers=[7])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[7],
    test_pc=_gnb_test_pc_0,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.68.89.23",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.23", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=830, global_bts_id=830)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# Concurrent ENB 1
_enb_pdu_1 = FACOM(addr="10.68.87.106", port_numbers=[2])
_enb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.115", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_enb_common_unit_1 = CommonUnit(
    lmp_connection=_enb_lmp_connection_1,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[2],
    test_pc=_enb_test_pc_1,
    hardware_type=None,
)
_real_enb_1 = Airscale(common_units=[_enb_common_unit_1])
_lte_real_enb_1 = RealEnb(
    system_module=_real_enb_1,
    oam_ip=NetworkAddress(v4="10.68.89.8"),
    instance_id=48830,
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

_netact = Netact("10.107.178.214")


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
