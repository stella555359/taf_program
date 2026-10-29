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
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Wang David"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "david.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.28",
        username="root",
        password="nokia123",
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
# 5GRU for classicalBTS
_ru_pdu_1 = HBTE(addr="10.68.87.104", port_numbers=[3])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[3],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.89.12", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.87.106", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_1], f1_m_ip_addr="10.68.89.12")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.12", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.12", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.89.11", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, global_bts_id=806, instance_id=806
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=806, global_bts_id=806)
_netact = Netact("10.110.144.147")

# CI_Detail_UE_Type='LG'
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57806,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.33", username="nokia5G", password="noki@123"
    ),
    serial_number="LMV500Ne42927a6",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "lg_v50"],
)

_appserver_ul = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ul,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=58806,
)
tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    nms=_netact,
)
