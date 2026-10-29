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
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.dcap import DcapRnD, DcapBasic

# ==================================================================================
# This example include MORAN/DUAL CORE/ CONCURRENT/ NR ONLY/ X2 ENB testline format.
# ==================================================================================

__maintainer__ = "zhu xiaofeng"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__email__ = "xiaofeng.1.zhu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.43", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# 5G RU for classicalBTS
_ru_0_pdu = FACOM(addr="10.68.87.180", port_numbers=[2])
_ru_0 = RU(
    ru_hw_group="AEWB",
    serial_number="AH220602871",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.64", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[2],
)
_ru_1_pdu = FACOM(addr="10.68.87.180", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AWEUC",
    serial_number="AH221600461",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.69", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
)
_ru_2_pdu = FACOM(addr="10.68.87.178", port_numbers=[5])
_ru_2 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2235G14FK",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[5],
)
# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_0 = HBTE(addr="10.68.87.90", port_numbers=[7])
_gnb_pdu_1 = HBTE(addr="10.68.87.90", port_numbers=[7])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.43", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.36", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[7],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[7],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru_0, _ru_1, _ru_2],
    f1_m_ip_addr="10.101.48.94",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="10.101.48.94",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.94",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.94",
        username="Nemuadmin",
        password="nemuuser",
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=748)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIL_DUALCORE"

# Netact IP
_netact = Netact("10.108.248.82")

# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
_enb_pdu_0 = FACOM(addr="10.68.87.90", port_numbers=[1])
_enb_lmp_connection_0 = SshServiceDetails(
    addr="10.101.48.93", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[1],
    test_pc=None,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb_0 = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.101.48.93"),
    instance_id=748,
    rms=[],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# Testline Summary
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_0],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
