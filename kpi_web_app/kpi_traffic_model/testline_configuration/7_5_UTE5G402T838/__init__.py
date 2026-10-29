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

__maintainer__ = "Shen jian"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jian.shen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.150", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_pdu = FACOM(addr="10.71.196.52", port_numbers=[4])
_ru_0 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL1933G10P1",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.51", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)

_ru_pdu1 = FACOM(addr="10.71.196.44", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AEHC",
    serial_number="L1202407695",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.109", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
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
_gnb_pdu_0 = HBTE(addr="10.71.196.45", port_numbers=[4])
_gnb_pdu_1 = HBTE(addr="10.71.196.45", port_numbers=[4])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.150", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.184", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    airscale=_gnb_airscale_0, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.71.211.198"
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.198", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=838)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# Concurrent ENB 0
_enb_pdu_0 = FACOM(addr="10.71.196.45", port_numbers=[3])
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.250", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[3],
    test_pc=_enb_test_pc_0,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb_0 = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.71.211.200"),
    instance_id=8382,
    rms=[_ru_0],
)

# ==================================================================================
# Concurrent ENB 1
_enb_pdu_1 = FACOM(addr="10.71.196.45", port_numbers=[3])
_enb_lmp_connection_common = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.73", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_enb_common_unit_1 = CommonUnit(
    lmp_connection=_enb_lmp_connection_common,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[3],
    test_pc=_enb_test_pc_1,
    hardware_type=None,
)

_real_enb_1 = Airscale(common_units=[_enb_common_unit_1])
_lte_real_enb_1 = RealEnb(
    system_module=_real_enb_1,
    oam_ip=NetworkAddress(v4="10.71.211.199"),
    instance_id=8381,
    rms=[_ru_1],
)

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
    port=57838,
)
_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="iperf",
    port=47838,
)
_appserver = AppServer(iperf_details=_iperf_ul)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.134", username="nokia5G", password="nokia123@"
    ),
    serial_number="R3CNC0FBFLH",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.134", username="nokia5G", password="nokia123@"
    ),
    serial_number="R5CN103KSWY",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_lte"],
)
_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.134", username="nokia5G", password="nokia123@"
    ),
    serial_number="RFCR40LFV6T",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.134", username="nokia5G", password="nokia123@"
    ),
    serial_number="RFCR40LFV6T",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_lte"],
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.28", port="1/6", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.68.85.28", port="1/3", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_0, _lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    ues=[_android_1, _android_2, _android_3, _android_4],
    appserver=_appserver,
)
