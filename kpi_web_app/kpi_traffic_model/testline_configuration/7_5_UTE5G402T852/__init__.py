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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Li Qing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "qing.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.8", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# PB for RU
_ru_pdu_1 = FACOM(addr="10.68.87.211", port_numbers=[5])
_ru_1 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2223G1AYG",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.29", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[5],
)

_ru_pdu_2 = FACOM(addr="10.68.87.55", port_numbers=[3])
_ru_2 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2116G1CH8",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.190", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[3],
)

_ru_pdu_3 = FACOM(addr="10.68.87.113", port_numbers=[6])
_ru_3 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2223G1B1H",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.50", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[6],
)

_ru_pdu_4 = FACOM(addr="10.68.87.110", port_numbers=[4])
_ru_4 = RU(
    ru_hw_group="AHFIG",
    serial_number="K9200425210",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.203", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[4],
)

_ru_pdu_5 = FACOM(addr="10.68.87.110", port_numbers=[6])
_ru_5 = RU(
    ru_hw_group="AHFIG",
    serial_number="BL2233W2D5X",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.132", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[6],
)

_ru_pdu_6 = FACOM(addr="10.68.87.110", port_numbers=[5])
_ru_6 = RU(
    ru_hw_group="AHFIG",
    serial_number="BL2050W2LFL",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.212", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[5],
)

_ru_pdu_7 = FACOM(addr="10.68.87.212", port_numbers=[1])
_ru_7 = RU(
    ru_hw_group="AEHC",
    serial_number="L1204110680",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.185", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[1],
)

_ru_pdu_8 = FACOM(addr="10.68.87.211", port_numbers=[1])
_ru_8 = RU(
    ru_hw_group="AEHC",
    serial_number="L1202407696",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.27", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[1],
)

_ru_pdu_9 = FACOM(addr="10.68.87.214", port_numbers=[6])
_ru_9 = RU(
    ru_hw_group="AEHC",
    serial_number="L1203404645",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", 
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.24", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu_9.pdu_ports[6],
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
_gnb_pdu_0 = HBTE(addr="10.68.87.61", port_numbers=[8])
_gnb_pdu_1 = HBTE(addr="10.68.87.61", port_numbers=[6])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.8", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.30", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[8],
    test_pc=_gnb_test_pc_0,
)
_gnb_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[6],
    test_pc=_gnb_test_pc_1,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0, _gnb_common_unit_1])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9],
    f1_m_ip_addr="10.101.48.49",
)
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.49", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=852)


# ==================================================================================
# Concurrent ENB 1
_enb_pdu_1 = FACOM(addr="10.68.87.61", port_numbers=[3])
_enb_lmp_connection_common = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.32", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    oam_ip=NetworkAddress(v4="10.101.48.37"),
    instance_id=48522,
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.28", port="1/12", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

_netact = Netact("10.107.178.214")

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57291,
)

# remote UE CPC
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.47", username="nokia5G", password="noki@123"
    ),
    serial_number="4b50ae0",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[_android],
    switches=[_dell_s4048on_switch],
)
