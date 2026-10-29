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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Hong liping"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "liping.hong@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.172",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.172",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

External_PCs_For_CellTrace = dict(docker=_docker_pc, tce=_tce_pc)
_HOTarget_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.87", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# 5GRU for classicalBTS

# PB for RU
_ru_pdu = FACOM(addr="10.57.241.233", port_numbers=[6])
_ru = RU(
    ru_hw_group="AEQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="w@=EIj7P6R0bVy85OjCVa^ho&8",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# GNB 0
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu_0 = FACOM(addr="10.57.241.232", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru],
    f1_m_ip_addr="10.57.151.238",
)

# gNB OAM M-plane IP
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.238", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.238", username="Nemuadmin", password="nemuuser"
    ),
)
# classicalbts
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=849, global_bts_id=849
)

# RealEnb
_enb_pdu_1 = FACOM(addr="10.57.241.233", port_numbers=[5])
_enb_lmp_connection_1 = SshServiceDetails(
    addr="10.57.151.27", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_1 = CommonUnit(
    lmp_connection=_enb_lmp_connection_1,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[5],
    hardware_type=None,
)
_real_enb_1 = Airscale(common_units=[_enb_common_unit_1])
_lte_real_enb_1 = RealEnb(
    airscale=_real_enb_1,
    rms=None,
    oam_ip=NetworkAddress(v4="10.57.151.27"),
    system_module=_real_enb_1,
    global_bts_id=10255,
    instance_id=10255,
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57849,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.150", username="nokia5G", password="noki@123"
    ),
    # serial_number="LMV500Ne45febac",
    serial_number="LMV500N705e3870",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "lg_v50"],
)

_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    test_pcs=[_HOTarget_pc, _docker_pc, _tce_pc],
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[
        _android,
    ],
    appserver=_appserver_ssh,
)
