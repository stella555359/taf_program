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

__maintainer__ = "Chen Yin 4"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com>"
__email__ = "yin.4.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.40", port="443", username="dcapuser", password="dcapadmin!"
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
_ru_pdu_1 = HBTE(addr="10.68.87.104", port_numbers=[5])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.157.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[5],
)

_ru_pdu_2 = FACOM(addr="10.68.87.56", port_numbers=[4])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    pdu_port=_ru_pdu_2.pdu_ports[4],
)

_ru_pdu_3 = FACOM(addr="10.68.87.124", port_numbers=[3])
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.157.32", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[3],
)

# DU1 for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.89.10", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu_1 = HBTE(addr="10.68.87.106", port_numbers=[5])
_gnb_pdu_2 = HBTE(addr="10.68.87.106", port_numbers=[7])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_1.pdu_ports[5],
)
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_2.pdu_ports[7],
)
_airscale = Airscale(common_units=[_common_unit_1, _common_unit_2])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.68.89.10")

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.10", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.10", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts_807 = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=10117, global_bts_id=10117
)

# RealEnb
_enb_pdu = FACOM(addr="10.68.87.107", port_numbers=[8])
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.88.246", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_enb = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[8],
)
_real_enb = Airscale(common_units=[_common_unit_enb])
_lte_real_enb = RealEnb(airscale=_real_enb)

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57807,
)

_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="iperf",
    port=47807,
)

_appserver = AppServer(iperf_details=_iperf_ul)

_mate = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.38", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19912001515",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_honor = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.23", username="CNHZ5GRAN1265+tester", password="tester123"
    ),
    serial_number="9EQUT21114001002",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "honor"],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc, _dcap_1],
    gnbs=[_classical_bts_807],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIB_ABIO_AEQN",
    ues=[_honor, _mate],
    appserver=_appserver,
)
