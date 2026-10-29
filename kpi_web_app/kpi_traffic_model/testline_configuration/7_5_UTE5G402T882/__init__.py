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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, MME, AMF, RealCore
from taf.config.testline import RU, DU, AppServer
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

__maintainer__ = "Xie Jia"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"  # TL owner's team
__email__ = "jia.xie@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.17", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu4 = HBTE(addr="10.71.196.56", port_numbers=[1])
_ru1 = RU(
    ru_hw_group="AHLOB",
    serial_number="BL2243D50X1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.42", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[1],
)
_ru_pdu5 = HBTE(addr="10.71.196.58", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="AHLOB",
    serial_number="BL2236D50B4",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.40", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[1],
)
_ru_pdu6 = HBTE(addr="10.71.196.58", port_numbers=[2])
_ru3 = RU(
    ru_hw_group="AHLOB",
    serial_number="BL2236D50B7",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.78", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[2],
)
_ru_pdu7 = HBTE(addr="10.71.196.56", port_numbers=[2])
_ru4 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2340N49YV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.41", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu7.pdu_ports[2],
)
_ru_pdu8 = HBTE(addr="10.71.196.58", port_numbers=[4])
_ru5 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2316N44V1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.38", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu8.pdu_ports[4],
)
_ru_pdu9 = HBTE(addr="10.71.196.58", port_numbers=[5])
_ru6 = RU(
    ru_hw_group="AHFII",
    serial_number="BL2340N49Z1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="rfsw",
        password="7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.39", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu9.pdu_ports[5],
)
_ru_pdu1 = HBTE(addr="10.71.196.56", port_numbers=[5])
_ru7 = RU(
    ru_hw_group="AEHC",
    serial_number="L1211203150",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.43", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
)
_ru_pdu2 = HBTE(addr="10.71.196.58", port_numbers=[6])
_ru8 = RU(
    ru_hw_group="AEHC",
    serial_number="L1211203219",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.44", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
)
_ru_pdu3 = HBTE(addr="10.71.196.58", port_numbers=[3])
_ru9 = RU(
    ru_hw_group="AEHC",
    serial_number="AH234900459",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.37", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)
_ru_pdu10 = HBTE(addr="10.71.196.56", port_numbers=[4])
_ru10 = RU(
    ru_hw_group="AVQQA",
    serial_number="L1242100640",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.52", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu10.pdu_ports[4],
)
_ru_pdu11 = HBTE(addr="10.71.196.56", port_numbers=[3])
_ru11 = RU(
    ru_hw_group="AVQQA",
    serial_number="L1242100641",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.53", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu11.pdu_ports[3],
)
_ru_pdu12 = HBTE(addr="10.71.196.46", port_numbers=[3])
_ru12 = RU(
    ru_hw_group="AVQQA",
    serial_number="L1243606660",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.172", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu12.pdu_ports[3],
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
_gnb_pdu_0 = HBTE(addr="10.71.196.46", port_numbers=[4])
_gnb_pdu_1 = HBTE(addr="10.71.196.46", port_numbers=[4])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.17", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.34", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[4],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[4],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11, _ru12],
    f1_m_ip_addr="10.71.211.205",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.205", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.205", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=882)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
# _enb_pdu_0 = FACOM(addr="10.57.241.164", port_numbers=[3])
# _enb_lmp_connection_0 = SshServiceDetails(
#     addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
# )

# _enb_test_pc_0 = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.167.103", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
# _enb_common_unit_0 = CommonUnit(
#     lmp_connection=_enb_lmp_connection_0,
#     capacity_units=[],
#     pdu_port=_enb_pdu_0.pdu_ports[3],
#     test_pc=_enb_test_pc_0,
#     hardware_type=None,
# )
# _real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
# _lte_real_enb_0 = RealEnb(
#     system_module=_real_enb_0,
#     oam_ip=NetworkAddress(v4="10.57.236.227"),
#     instance_id=4090,
# )

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# ==================================================================================
# ==================================================================================
# ==================================================================================
# UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57882,
)
_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="iperf",
    port=47882,
)
_appserver = AppServer(iperf_details=_iperf_ul)
# CI_Detail_UE_Type='Samsung'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.158", username="mn5gran", password="nokia123@"
    ),
    serial_number="L1211203150",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.158", username="mn5gran", password="nokia123@"
    ),
    serial_number="L1211203150",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_lte"],
)
_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.166", username="mn5gran", password="nokia123@"
    ),
    serial_number="BL2236D50AY",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.166", username="mn5gran", password="nokia123@"
    ),
    serial_number="BL2236D50AY",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_lte"],
)
## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.71.211.193", port="1/6", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)
_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
    ues=[_android_1, _android_2, _android_3, _android_4],
    appserver=_appserver,
)
