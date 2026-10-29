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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Qu Jing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jing.qu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.82", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
# 5GRU for classicalBTS

# PB for RU
_ru_pdu = FACOM(addr="10.57.241.230", port_numbers=[3, 6])
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw="
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu.pdu_ports[3],
)
_ru_pdu_2 = FACOM(addr="10.57.241.228", port_numbers=[2])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu_2.pdu_ports[2],
)
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu.pdu_ports[6],
)
_ru_pdu_4 = FACOM(addr="10.57.172.216", port_numbers=[6])
_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu_4.pdu_ports[6],
)
_ru_pdu_5 = FACOM(addr="10.57.172.223", port_numbers=[2])
_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu_5.pdu_ports[2],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.57.241.232", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru_2, _ru_3, _ru_4, _ru_5], f1_m_ip_addr="10.57.151.239")

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.239", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.239", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_pdu = FACOM(addr="10.57.241.233", port_numbers=[7])
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.151.6", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[7],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, global_bts_id=10283, instance_id=10283
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10565, global_bts_id=10565)

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57853,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.14", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19909000046",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="iperf",
    port=47853,
)

_appserver = AppServer(iperf_details=_iperf_ul)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    appserver=_appserver,
)
